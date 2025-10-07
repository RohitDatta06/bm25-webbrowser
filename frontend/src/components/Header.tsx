export default function Header() {
return (
    <header className="sticky top-0 z-10 border-b border-gray-200 bg-white/80 backdrop-blur">
    <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
    <div className="flex items-center gap-2">
    <div className="h-8 w-8 rounded-xl bg-blue-600" />
    <h1 className="text-lg font-semibold">BM25 Search</h1>
    </div>
    <a className="text-sm text-blue-600 hover:underline" href="https://render.com" target="_blank">Hosted on Render</a>
    </div>
    </header>
)
}