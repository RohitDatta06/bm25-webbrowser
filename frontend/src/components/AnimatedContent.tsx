import { useEffect, useRef } from 'react'

type Props = {
  children: React.ReactNode
  distance?: number
  direction?: 'horizontal' | 'vertical'
  reverse?: boolean
  duration?: number
  ease?: string
  initialOpacity?: number
  animateOpacity?: boolean
  scale?: number
  threshold?: number
  delay?: number
}

export default function AnimatedContent({
  children,
  distance = 100,
  direction = 'vertical',
  reverse = false,
  duration = 1.0,
  initialOpacity = 0.2,
  animateOpacity = true,
  scale = 1,
  threshold = 0.2,
  delay = 0,
}: Props) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const startX = direction === 'horizontal' ? (reverse ? -distance : distance) : 0
    const startY = direction === 'vertical' ? (reverse ? -distance : distance) : 0
    el.style.opacity = String(initialOpacity)
    el.style.transform = `translate(${startX}px, ${startY}px) scale(${scale})`
    el.style.transition = `transform ${duration}s cubic-bezier(.22,.61,.36,1), opacity ${duration}s ease`
    el.style.transitionDelay = `${delay}s`

    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          el.style.opacity = animateOpacity ? '1' : String(initialOpacity)
          el.style.transform = 'translate(0, 0) scale(1)'
          io.disconnect()
        }
      })
    }, { threshold })
    io.observe(el)
    return () => io.disconnect()
  }, [distance, direction, reverse, duration, initialOpacity, animateOpacity, scale, threshold, delay])

  return <div ref={ref}>{children}</div>
}
