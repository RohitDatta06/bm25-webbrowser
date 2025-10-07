import { useEffect, useRef, useState } from 'react'

type Props = {
  items: string[]
  children?: React.ReactNode
  onItemSelect?: (item: string, index: number) => void
  showGradients?: boolean
  enableArrowNavigation?: boolean
  displayScrollbar?: boolean
}

export default function AnimatedList({
  items,
  children,
  onItemSelect,
  showGradients = true,
  enableArrowNavigation = true,
  displayScrollbar = true,
}: Props) {
  const ref = useRef<HTMLDivElement>(null)
  const [idx, setIdx] = useState(0)

  useEffect(() => {
    if (!enableArrowNavigation) return
    function onKey(e: KeyboardEvent) {
      if (e.key === 'ArrowDown') setIdx(i => Math.min(i + 1, items.length - 1))
      if (e.key === 'ArrowUp') setIdx(i => Math.max(i - 1, 0))
      if (e.key === 'Enter') onItemSelect?.(items[idx], idx)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [items, idx, enableArrowNavigation])

  return (
    <div
      ref={ref}
      className={`relative ${displayScrollbar ? 'overflow-y-auto' : 'overflow-hidden'} max-h-[70vh] rounded-2xl border border-gray-200 p-2`}
    >
      {showGradients && (
        <>
          <div className="pointer-events-none absolute inset-x-0 top-0 h-6 bg-gradient-to-b from-white to-transparent" />
          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-6 bg-gradient-to-t from-white to-transparent" />
        </>
      )}
      {children}
    </div>
  )
}
