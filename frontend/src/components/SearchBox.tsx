import { FormEvent } from 'react'


export default function SearchBox({ value, setValue, onSubmit }: { value: string; setValue: (v: string) => void; onSubmit: () => void }) {
    function submit(e: FormEvent) {
    e.preventDefault();
    onSubmit();
    }
    return (
        <form onSubmit={submit} className="flex items-center gap-2">
        <input
        className="input"
        placeholder="Try: robotics reinforcement learning"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        aria-label="Search query"
        />
        <button type="submit" className="btn btn-primary">Search</button>
        </form>
        )
}