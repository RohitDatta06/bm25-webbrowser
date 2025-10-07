import { useEffect, useRef, useState } from 'react'

type Props = {
  text: string[]
  typingSpeed?: number
  pauseDuration?: number
  showCursor?: boolean
  cursorCharacter?: string
}

export default function TextType({
  text,
  typingSpeed = 75,
  pauseDuration = 1500,
  showCursor = true,
  cursorCharacter = '|',
}: Props) {
  const [idx, setIdx] = useState(0)
  const [sub, setSub] = useState('')
  const [phase, setPhase] = useState<'typing' | 'pausing' | 'deleting'>('typing')
  const timer = useRef<number>()

  useEffect(() => {
    const current = text[idx % text.length]
    if (phase === 'typing') {
      if (sub.length < current.length) {
        timer.current = window.setTimeout(() => setSub(current.slice(0, sub.length + 1)), typingSpeed)
      } else {
        setPhase('pausing')
        timer.current = window.setTimeout(() => setPhase('deleting'), pauseDuration)
      }
    } else if (phase === 'deleting') {
      if (sub.length > 0) {
        timer.current = window.setTimeout(() => setSub(sub.slice(0, -1)), typingSpeed / 2)
      } else {
        setPhase('typing')
        setIdx(i => i + 1)
      }
    }
    return () => clearTimeout(timer.current)
  }, [sub, phase, idx, text, typingSpeed, pauseDuration])

  return (
    <span>
      {sub}{showCursor && <span className="opacity-60">{cursorCharacter}</span>}
    </span>
  )
}
