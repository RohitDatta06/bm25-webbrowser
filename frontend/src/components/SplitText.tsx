import { useEffect, useRef } from 'react'

type Props = {
  text: string
  className?: string
  delay?: number
  duration?: number
  ease?: string
  splitType?: 'chars' | 'words'
  from?: Partial<CSSStyleDeclaration> | { opacity?: number; y?: number }
  to?: Partial<CSSStyleDeclaration> | { opacity?: number; y?: number }
  threshold?: number
  rootMargin?: string
  textAlign?: 'left' | 'center' | 'right'
  onLetterAnimationComplete?: () => void
}

export default function SplitText({
  text,
  className='',
  delay=30,
  duration=0.5,
  splitType='chars',
  from={ opacity: 0, y: 20 },
  to={ opacity: 1, y: 0 },
  threshold=0.1,
  rootMargin='-100px',
  textAlign='left',
  onLetterAnimationComplete,
}: Props) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const items = Array.from(el.querySelectorAll('[data-chunk]')) as HTMLElement[]
    items.forEach((s, i) => {
      s.style.opacity = String((from as any).opacity ?? 0)
      s.style.transform = `translateY(${(from as any).y ?? 20}px)`
      s.style.transition = `transform ${duration}s ease, opacity ${duration}s ease`
      s.style.transitionDelay = `${i * delay / 1000}s`
    })
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          items.forEach(s => {
            s.style.opacity = String((to as any).opacity ?? 1)
            s.style.transform = `translateY(${(to as any).y ?? 0}px)`
          })
          setTimeout(() => onLetterAnimationComplete?.(),
            (items.length * delay) + duration * 1000)
          io.disconnect()
        }
      })
    }, { threshold, rootMargin })
    io.observe(el)
    return () => io.disconnect()
  }, [text])

  const chunks = splitType === 'words' ? text.split(/(\s+)/) : Array.from(text)
  return (
    <div ref={ref} className={className} style={{ textAlign }}>
      {chunks.map((c, i) =>
        c === ' '
          ? <span key={i}> </span>
          : <span key={i} data-chunk className="inline-block will-change-transform">{c}</span>
      )}
    </div>
  )
}
