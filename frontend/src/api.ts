const API_BASE = import.meta.env.VITE_API_BASE || window.location.origin


export type SearchHit = {
    doc_id: number
    score: number
    url: string
    title: string
}


export async function search(q: string, k = 10): Promise<SearchHit[]> {
    const u = new URL('/search', API_BASE)
    u.searchParams.set('q', q)
    u.searchParams.set('k', String(k))
    const r = await fetch(u.toString(), { headers: { 'Accept': 'application/json' } })
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    const data = await r.json()
    return data.results as SearchHit[]
}