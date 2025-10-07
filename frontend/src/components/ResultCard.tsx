import type { SearchHit } from '../api'


function highlight(text: string, q: string) {
    if (!q) return text
    try {
        const terms = q.split(/\s+/).filter(Boolean).map(t => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
        const re = new RegExp(`(${terms.join('|')})`, 'ig')
        return text.split(re).map((chunk, i) => (
        re.test(chunk) ? <mark key={i} className="bg-yellow-200 px-0.5">{chunk}</mark> : <span key={i}>{chunk}</span>
        ))
    } catch { return text }
}


export default function ResultCard({ hit, q }: { hit: SearchHit; q: string }) {
    const host = (() => { try { return new URL(hit.url).host } catch { return '' } })()
    return (
        <li className="card">
        <a href={hit.url} target="_blank" className="block">
        <div className="text-sm text-gray-500">{host}</div>
        <div className="mt-1 text-lg font-medium text-blue-700 hover:underline">{hit.title || hit.url}</div>
        </a>
        <div className="mt-1 text-xs text-gray-500">score {hit.score.toFixed(4)}</div>

        </li>
)
}