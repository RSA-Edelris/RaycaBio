/**
 * Personas from the registry, ranked against the task.
 *
 * THE REGISTRY IS THE SOURCE. A hand-written roster drifts the first time a persona is added, and the registry already
 * holds 122 of them with a summary and a category each.
 */

import { readFileSync } from 'node:fs';

const REGISTRY = process.env.RAYCA_PERSONAS || '/home/ubuntu/.rayca-library/parsed-personas.json';

export function loadPersonas(path = REGISTRY) {
  try {
    const raw = JSON.parse(readFileSync(path, 'utf8'));
    const rows = Array.isArray(raw) ? raw : raw.rows || [];
    return rows.filter((r) => r && r.id && r.name).map((r) => ({
      id: String(r.id),
      name: String(r.name),
      summary: String(r.summary || ''),
      category: String(r.category_label || r.category || ''),
    }));
  } catch (e) {
    process.stderr.write('[max] could not read the persona registry: ' + e.message + '\n');
    return [];
  }
}

const STOP = new Set(['the', 'and', 'for', 'with', 'this', 'that', 'from', 'what', 'which', 'their', 'using', 'into',
  'have', 'about', 'would', 'should', 'could', 'each', 'them', 'then', 'than', 'over', 'more', 'only', 'also', 'said',
  'they', 'been', 'were', 'will', 'when', 'your', 'them', 'these', 'those', 'such', 'both', 'does']);

/**
 * Rank by how much of the task's own language a persona covers.
 *
 * WHY RANKING AT ALL. The first version of team formation in the engine took the registry's first N rows, which staffed
 * a chemistry question with a privacy lawyer. Ties keep registry order so the result is stable, and a persona matching
 * nothing is dropped rather than padded in: a smaller team of specialists beats a full team of bystanders.
 */
export function rankPersonas(personas, task, n = 4) {
  const words = new Set((String(task).toLowerCase().match(/[a-z][a-z-]{3,}/g) || []).filter((w) => !STOP.has(w)));
  const scored = personas.map((p, i) => {
    const hay = (p.name + ' ' + p.summary + ' ' + p.category).toLowerCase();
    let hits = 0;
    for (const w of words) if (hay.includes(w)) hits += 1;
    return { p, hits, i };
  });
  scored.sort((a, b) => (b.hits - a.hits) || (a.i - b.i));
  const picked = scored.filter((s) => s.hits > 0).slice(0, n);
  return (picked.length ? picked : scored.slice(0, Math.min(2, scored.length))).map((s) => s.p);
}
