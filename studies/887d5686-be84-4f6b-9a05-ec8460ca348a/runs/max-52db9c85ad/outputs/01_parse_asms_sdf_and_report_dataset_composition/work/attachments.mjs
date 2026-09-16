/**
 * WHAT THE RESEARCHER ATTACHED, MADE REACHABLE BY THE MODEL.
 *
 * MEASURED, and the operator has now reported it twice: "the attachement of the composer box do not reach the engine, doean't
 * matter if they are attached files or attached skills, containerized tools and persona or files added to the composer from file
 * manager, non of the reach the engine."
 *
 * They were half right, and the half that was wrong is the interesting half. The console DOES send them: `startExtras()` puts
 * `attachments: [...]` on the run request and the intervention request. `grep attachments server.mjs` returned NOTHING. The field
 * arrived on every run and was read by nobody, so a chip in the composer was a promise the engine never heard.
 *
 * WHAT AN ATTACHMENT ACTUALLY IS ON THE WIRE: `{ kind, id, name, category_label }`. Four strings. No content, no path, no schema.
 * That is the right thing to send, because the alternative is the browser posting a skill's full text back to the machine that
 * already has it, but it means the engine has to RESOLVE each one, and each kind lives somewhere different:
 *
 *   files       the session workspace, found by name, because that is where the file manager's files already are
 *   tools       TOOLKIT_ROOT/tools/<id>/tool.yaml and io_schema.json, which is what a container tool is
 *   pipelines   TOOLKIT_ROOT/pipelines/<id>/pipeline.yaml
 *   skills      the registry's skills tree, nested under collections, so found by walking rather than by joining a path
 *   personas    the parsed personas index the engine already loads for team selection
 *   frameworks  the parsed frameworks index, keyed by the dotted id the console sends
 *   databases   the registry's databases tree, one DATABASE.md per source
 *
 * WHY A BRIEFING RATHER THAN A TOOL PER ATTACHMENT. The model already has verbs for running containers, reading files and
 * searching memory. What it lacked was the knowledge that the researcher had SINGLED SOMETHING OUT. So each resolved attachment
 * becomes a line of instruction naming the thing, where it is, and what to do with it, and that text goes into the task. It needs
 * no new plumbing in the loop and it survives compaction, because it is part of what was asked.
 *
 * ANYTHING THAT CANNOT BE RESOLVED IS SAID OUT LOUD, in the briefing and in an event. A chip that silently resolves to nothing is
 * the defect this file exists to fix, and replacing it with a chip that silently resolves to almost nothing would be no better.
 */
import fs from 'node:fs';
import path from 'node:path';

const TOOLKIT = process.env.TOOLKIT_ROOT || '/home/ubuntu/rayca-toolkit';
const LIBRARY = process.env.RAYCA_LIBRARY || '/home/ubuntu/.rayca-library';
const REGISTRY = path.join(LIBRARY, 'registry');
const ENGRAMS = path.join(LIBRARY, 'frameworks', 'engrams');
/* Where uploaded and registered files live, which is NOT the session workspace. */
const ARTIFACTS = process.env.RAYCA_ARTIFACTS_ROOT || '/home/ubuntu/rayca-artifacts';

/*
 * CAPS, BECAUSE A SKILL IS A DOCUMENT. `SKILL.md` and `DATABASE.md` run to thousands of words, and pasting four of them into a
 * task would spend the context the run needs on material the model can read for itself once it knows the path. Each item gets
 * enough to act on and is told where the rest is.
 */
const PER_ITEM_CHARS = 1200;
const TOTAL_CHARS = 12000;

function readIfFile(p, limit = PER_ITEM_CHARS) {
  try {
    if (!fs.statSync(p).isFile()) {
      return '';
    }
    const text = fs.readFileSync(p, 'utf8');
    return text.length > limit ? `${text.slice(0, limit)}\n[truncated, the full text is at ${p}]` : text;
  } catch {
    return '';
  }
}

/** The first paragraph that is not a heading, which is what a summary line wants. */
function summarise(text, limit = 400) {
  const body = String(text || '')
    .split('\n')
    .filter((l) => l.trim() && !l.trim().startsWith('#') && !l.trim().startsWith('---'))
    .join(' ')
    .trim();
  return body.length > limit ? `${body.slice(0, limit)}...` : body;
}

/**
 * A DIRECTORY NAMED `id`, FOUND BY WALKING RATHER THAN BY JOINING.
 *
 * The skills and databases trees group their items under collection directories, so the path of an item cannot be derived from its
 * id. Bounded depth and an early return, because this runs on the request path and the trees are large.
 */
function findDir(root, id, depth = 3) {
  const wanted = String(id || '');
  if (!wanted) {
    return '';
  }
  const stack = [{ dir: root, left: depth }];
  while (stack.length) {
    const { dir, left } = stack.pop();
    let entries = [];
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const e of entries) {
      if (!e.isDirectory()) {
        continue;
      }
      if (e.name === wanted) {
        return path.join(dir, e.name);
      }
      if (left > 1) {
        stack.push({ dir: path.join(dir, e.name), left: left - 1 });
      }
    }
  }
  return '';
}

/** A file of this name anywhere under the workspace, which is where the file manager's files already live. */
function findFile(root, name, depth = 4) {
  const wanted = String(name || '');
  if (!root || !wanted) {
    return '';
  }
  const stack = [{ dir: root, left: depth }];
  while (stack.length) {
    const { dir, left } = stack.pop();
    let entries = [];
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const e of entries) {
      if (e.isFile() && e.name === wanted) {
        return path.join(dir, e.name);
      }
      /* `.remember` holds the run's own bookkeeping and is not the researcher's data. */
      if (e.isDirectory() && left > 1 && !e.name.startsWith('.')) {
        stack.push({ dir: path.join(dir, e.name), left: left - 1 });
      }
    }
  }
  return '';
}

/*
 * ANOTHER SESSION'S WORKSPACE, FOUND BY ITS KEY.
 *
 * A workspace directory is the session key with a suffix, so the key alone does not give the path and it has to be matched by
 * prefix. Read from the sessions root rather than asked of the platform, because this runs while a request is being answered and a
 * bridge round trip on that path has already been seen to time out and lose data.
 */
const SESSIONS_ROOT = process.env.RAYCA_SESSIONS_ROOT || '/home/ubuntu/rayca-sessions';

export function sessionWorkspace(sessionKey) {
  const key = String(sessionKey || '');
  if (!key) {
    return '';
  }
  try {
    const hit = fs.readdirSync(SESSIONS_ROOT, { withFileTypes: true })
      .find((e) => e.isDirectory() && (e.name === key || e.name.startsWith(`${key}-`)));
    return hit ? path.join(SESSIONS_ROOT, hit.name) : '';
  } catch {
    return '';
  }
}

function jsonIndex(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return null;
  }
}

/** Every record in a parsed index, whatever nesting it uses, so a lookup by id does not depend on its shape. */
function flattenRecords(node, out = []) {
  if (Array.isArray(node)) {
    for (const x of node) {
      flattenRecords(x, out);
    }
  } else if (node && typeof node === 'object') {
    if (typeof node.id === 'string') {
      out.push(node);
    }
    for (const v of Object.values(node)) {
      if (v && typeof v === 'object') {
        flattenRecords(v, out);
      }
    }
  }
  return out;
}

let personaCache = null;
let frameworkCache = null;

function lookupIndexed(kind, id) {
  if (kind === 'personas') {
    personaCache = personaCache || flattenRecords(jsonIndex(path.join(LIBRARY, 'parsed-personas.json')));
    return (personaCache || []).find((r) => r.id === id) || null;
  }
  frameworkCache = frameworkCache || flattenRecords(jsonIndex(path.join(LIBRARY, 'parsed-frameworks.json')));
  return (frameworkCache || []).find((r) => r.id === id) || null;
}

/** Text worth putting in front of the model for one record from a parsed index. */
function recordText(rec) {
  if (!rec) {
    return '';
  }
  const parts = [rec.summary, rec.description, rec.purpose, rec.when_to_use, rec.method, rec.headline]
    .filter((v) => typeof v === 'string' && v.trim());
  return summarise(parts.join(' '), PER_ITEM_CHARS);
}

/**
 * RESOLVE ONE ATTACHMENT.
 *
 * Returns what the briefing needs plus enough to say honestly that it could not be found. `where` is the thing that makes an
 * attachment actionable: a path the model can open, or a registry id it can name to another verb.
 */
export function resolveOne(item, { workspace = '', registry = null } = {}) {
  const kind = String(item?.kind || '');
  const id = String(item?.id || '');
  const name = String(item?.name || id);
  const base = { kind, id, name, found: false, where: '', detail: '' };

  /*
   * `file` AND `files`, BECAUSE THE CONSOLE SAYS `file`.
   *
   * MEASURED, reported by the operator after attaching an image both ways: 'system marked it "unrecognised attachment kind file"'.
   * I wrote the plural. Both senders, the File Manager section and the composer's upload button, add `kind: 'file'` singular, so every
   * file attachment ever made fell through to the unknown-kind branch. The one kind a researcher reaches for most was the one kind
   * that could not resolve.
   *
   * Both spellings are accepted rather than one being corrected, because the wire is a contract between two deployables that ship
   * separately: an engine that only understood the new spelling would break every console older than itself.
   */
  if (kind === 'files' || kind === 'file') {
    /*
     * A FILE MAY BELONG TO ANOTHER SESSION, and the console says so when it does.
     *
     * The file manager lets a reader pick a file out of a different study's workspace, and the attachment then carries the session it
     * came from. Looking only in the current workspace would make exactly those attachments unresolvable, which is the more valuable
     * half of the feature: bringing a result forward from earlier work is why someone reaches for the file manager at all.
     */
    const home = item?.session ? sessionWorkspace(String(item.session)) : '';
    /*
     * THE ARTIFACT REGISTRY IS ASKED FIRST, because it is the only thing that KNOWS.
     *
     * MEASURED: a file uploaded from a computer does not land in the session workspace at all. It lands under
     * `rayca-artifacts/<workspace id>/files/`, a second location keyed by an id that cannot be derived from the session key. So a
     * search of the workspace found produced files and missed every uploaded one, which is half of what a researcher attaches.
     *
     * The registry answers with the path and the id the console already sent, so the lookup is exact rather than by name. Directory
     * search stays as the fallback for a file that exists but was never registered.
     */
    const registered = registry ? registry(String(item?.id || ''), name) : '';
    const at = registered || findFile(workspace, name) || (home ? findFile(home, name) : '')
      || findFile(ARTIFACTS, name, 3);
    if (!at) {
      return { ...base, detail: 'attached in the composer but not found in this session workspace' };
    }
    let size = 0;
    try {
      size = fs.statSync(at).size;
    } catch { /* the path is what matters */ }
    return { ...base, found: true, where: at, detail: size ? `${size} bytes` : '' };
  }

  if (kind === 'tools') {
    const dir = path.join(TOOLKIT, 'tools', id);
    const spec = readIfFile(path.join(dir, 'tool.yaml'));
    if (!spec) {
      return { ...base, detail: 'not found in the container tool catalogue' };
    }
    const io = readIfFile(path.join(dir, 'io_schema.json'), 900);
    return { ...base, found: true, where: dir, detail: summarise(spec), schema: io };
  }

  if (kind === 'pipelines') {
    const dir = path.join(TOOLKIT, 'pipelines', id);
    const spec = readIfFile(path.join(dir, 'pipeline.yaml'));
    if (!spec) {
      return { ...base, detail: 'not found in the pipeline catalogue' };
    }
    return { ...base, found: true, where: dir, detail: summarise(spec) };
  }

  if (kind === 'skills') {
    const dir = findDir(path.join(REGISTRY, 'skills'), id);
    const text = dir ? readIfFile(path.join(dir, 'SKILL.md')) : '';
    if (!text) {
      return { ...base, detail: 'not found in the skills registry' };
    }
    return { ...base, found: true, where: path.join(dir, 'SKILL.md'), detail: summarise(text, PER_ITEM_CHARS) };
  }

  if (kind === 'databases') {
    const dir = findDir(path.join(REGISTRY, 'databases'), id);
    const text = dir ? readIfFile(path.join(dir, 'DATABASE.md')) : '';
    if (!text) {
      return { ...base, detail: 'not found in the database catalogue' };
    }
    return { ...base, found: true, where: path.join(dir, 'DATABASE.md'), detail: summarise(text, PER_ITEM_CHARS) };
  }

  if (kind === 'frameworks') {
    /*
     * THE ACTUAL ENGRAM, NOT A SUMMARY OF IT.
     *
     * The operator asked the right question: "operatonal frameworks for instance, shoud triget the memory procedural layer and raech
     * that specific engram." My first version injected the one-line summary from the parsed index, which tells the model a method
     * exists and not what the method IS.
     *
     * The id the console sends is the engram's path with dots where the slashes go, so it addresses the card directly:
     * `20-synthesis-planning.retrosynthetic-route-planning.folded-protein` is
     * `engrams/20-synthesis-planning/retrosynthetic-route-planning/folded-protein/card.md`. No search and no ranking, which matters
     * because the reader has already chosen: a similarity query against the procedural layer could return a NEIGHBOUR of what they
     * attached, and quietly following a method nobody asked for is worse than following none.
     *
     * The index stays as the fallback, for an id whose card is not on disk.
     */
    const card = path.join(ENGRAMS, ...id.split('.'), 'card.md');
    const text = readIfFile(card, PER_ITEM_CHARS * 2);
    if (text) {
      return { ...base, found: true, where: card, detail: text };
    }
    const rec = lookupIndexed('frameworks', id);
    if (!rec) {
      return { ...base, detail: 'no engram card on disk and not in the frameworks index' };
    }
    return { ...base, found: true, where: id, detail: recordText(rec) || String(rec.title || rec.name || id) };
  }

  if (kind === 'personas') {
    const rec = lookupIndexed('personas', id);
    if (!rec) {
      return { ...base, detail: 'not found in the personas index' };
    }
    return { ...base, found: true, where: id, detail: recordText(rec) || String(rec.title || rec.name || id) };
  }

  if (kind === 'plugins') {
    /* A published attachment kind that had no branch, so it reported itself unrecognised. Resolved from the registry's plugins tree. */
    const dir = findDir(path.join(REGISTRY, 'plugins'), id);
    const text = dir ? (readIfFile(path.join(dir, 'PLUGIN.md')) || readIfFile(path.join(dir, 'README.md'))) : '';
    if (!text) {
      return { ...base, detail: 'not found in the plugins registry' };
    }
    return { ...base, found: true, where: dir, detail: summarise(text, PER_ITEM_CHARS) };
  }

  return { ...base, detail: `unrecognised attachment kind "${kind}"` };
}

/*
 * A PREFERENCE, NOT A CAGE.
 *
 * The operator, and this changes the wording of every line below: "the attachemnts must not be the enforcement but a user preference,
 * if the model found better and more established tool or method or skill, then they should aslo adopt them in addition to the user
 * preferences."
 *
 * My first wording said "prefer these over writing an equivalent yourself" and "follow these rather than choosing your own approach",
 * which reads as a ceiling. It is the wrong instruction for two reasons. A researcher attaching a tool is saying "I trust this and I
 * want it used", not "consider nothing else"; and the platform's whole claim is that it knows methods a person has not thought of, so
 * an instruction that forbids it from bringing one is an instruction to be less useful than it is.
 *
 * So each heading now says: use this, AND add anything better established that you know of, and say why you added it. The last clause
 * is what keeps it honest rather than a licence to wander: an addition the reader cannot see the reason for is indistinguishable from
 * the model ignoring them.
 */
const ALSO = 'Use these. You may ALSO use a better established tool or method if you know one, in addition rather than instead, and say why you added it.';

/**
 * THE BRIEFING, WRITTEN AS INSTRUCTIONS RATHER THAN AS A MANIFEST.
 *
 * A list of names tells the model something was attached; it does not tell it what to do. So each kind gets a sentence saying how
 * that kind is meant to be used, because the answer differs: a file is to be read, a container tool is to be preferred over
 * writing the same thing in Python, a persona is a viewpoint to adopt, a framework is a method to follow.
 *
 * THE UNRESOLVED ONES ARE LISTED TOO. The model should say it cannot see a file rather than answer as though it had, which is
 * exactly what the operator hit: "I said read this file attached and the engine said I don't see any files."
 */
export function briefingFrom(resolved) {
  if (!resolved.length) {
    return '';
  }
  /* `file` and `files` are one group, since the console sends the singular and older tapes carry the plural. */
  const by = (k) => resolved.filter((r) => r.found && (r.kind === k || (k === 'files' && r.kind === 'file')));
  const lines = [];
  const push = (heading, items, render) => {
    if (!items.length) {
      return;
    }
    lines.push(heading);
    for (const r of items) {
      lines.push(render(r));
    }
    lines.push('');
  };

  push(
    `FILES THE RESEARCHER ATTACHED. Read these before answering, and if one is central to the question, read it first. If you need another file to answer properly, read that too and say so:`,
    by('files'),
    (r) => `- ${r.name} at ${r.where}${r.detail ? ` (${r.detail})` : ''}`,
  );
  push(
    `CONTAINER TOOLS THE RESEARCHER CHOSE, dispatched by name. ${ALSO}`,
    by('tools'),
    (r) => `- ${r.name}: ${r.detail}${r.schema ? `\n  inputs: ${r.schema}` : ''}`,
  );
  push(
    `PIPELINES THE RESEARCHER CHOSE. Run these rather than reimplementing the workflow. ${ALSO}`,
    by('pipelines'),
    (r) => `- ${r.name}: ${r.detail}`,
  );
  push(
    `SKILLS THE RESEARCHER ATTACHED, to be followed where they apply. ${ALSO}`,
    by('skills'),
    (r) => `- ${r.name}: ${r.detail}\n  full text: ${r.where}`,
  );
  push(
    `OPERATIONAL FRAMEWORKS THE RESEARCHER ATTACHED. These are the methods for the steps they cover. ${ALSO} If a framework and a better method disagree on a step, do both where the cost allows and report the difference rather than choosing silently.`,
    by('frameworks'),
    (r) => `- ${r.id}: ${r.detail}`,
  );
  push(
    `DATA SOURCES THE RESEARCHER CHOSE. Take the data from these. ${ALSO}`,
    by('databases'),
    (r) => `- ${r.name}: ${r.detail}\n  how to query it: ${r.where}`,
  );
  push(
    `EXPERTISE THE RESEARCHER ASKED FOR. Answer from these viewpoints, and delegate to them if the work divides. ${ALSO}`,
    by('personas'),
    (r) => `- ${r.name}: ${r.detail}`,
  );

  const missing = resolved.filter((r) => !r.found);
  if (missing.length) {
    lines.push(
      'ATTACHED BUT NOT RESOLVED. Say so in your answer rather than proceeding as though you had them, and do not invent their contents:',
    );
    for (const r of missing) {
      lines.push(`- ${r.kind} "${r.name}": ${r.detail}`);
    }
    lines.push('');
  }

  const body = lines.join('\n').trim();
  const capped = body.length > TOTAL_CHARS ? `${body.slice(0, TOTAL_CHARS)}\n[attachment briefing truncated]` : body;
  return `\n\n--- ATTACHED BY THE RESEARCHER ---\n${capped}\n--- END OF ATTACHMENTS ---\n`;
}

/**
 * Resolve a whole set. Never throws: an attachment that cannot be read must not take the run down with it, because the run is
 * still worth doing without it.
 */
export function resolveAttachments(items, opts = {}) {
  const list = Array.isArray(items) ? items.slice(0, 40) : [];
  const resolved = [];
  for (const it of list) {
    try {
      resolved.push(resolveOne(it, opts));
    } catch (e) {
      resolved.push({
        kind: String(it?.kind || ''), id: String(it?.id || ''), name: String(it?.name || ''),
        found: false, where: '', detail: `could not be read: ${String(e?.message || e).slice(0, 120)}`,
      });
    }
  }
  return { resolved, briefing: briefingFrom(resolved), found: resolved.filter((r) => r.found).length };
}

export default resolveAttachments;
