import { useEffect, useRef } from 'react'

export default function LiquidEther() {
  const ref = useRef<HTMLCanvasElement>(null)
  useEffect(() => {
    const canvas = ref.current!
    const ctx = canvas.getContext('2d')!
    let w = canvas.width = window.innerWidth
    let h = canvas.height = window.innerHeight
    const colors = ['#5227FF', '#FF9FFC', '#B19EEF']
    const blobs = Array.from({ length: 12 }, (_, i) => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: 120 + Math.random() * 140,
      vx: (Math.random() * 2 - 1) * 0.2,
      vy: (Math.random() * 2 - 1) * 0.2,
      c: colors[i % colors.length]
    }))
    const grad = ctx.createLinearGradient(0, 0, w, h)
    grad.addColorStop(0, '#fdfdfd')
    grad.addColorStop(1, '#f6f7fb')

    let raf = 0
    const draw = () => {
      ctx.fillStyle = grad
      ctx.fillRect(0, 0, w, h)
      blobs.forEach(b => {
        b.x += b.vx; b.y += b.vy
        if (b.x < -b.r) b.x = w + b.r; if (b.x > w + b.r) b.x = -b.r
        if (b.y < -b.r) b.y = h + b.r; if (b.y > h + b.r) b.y = -b.r
        const g = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r)
        g.addColorStop(0, b.c + '22')
        g.addColorStop(1, '#0000')
        ctx.fillStyle = g
        ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2); ctx.fill()
      })
      raf = requestAnimationFrame(draw)
    }
    draw()
    const onResize = () => { w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight }
    window.addEventListener('resize', onResize)
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', onResize) }
  }, [])
return (
  <canvas
    id="bg-canvas"
    ref={ref}
    aria-hidden="true"
    style={{ position:'fixed', inset:0, width:'100vw', height:'100vh', zIndex:-1, pointerEvents:'none' }}
  />
)

}
