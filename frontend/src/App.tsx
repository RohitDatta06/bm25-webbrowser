import { useEffect, useState } from "react";
import Header from "./components/Header";
import SearchBox from "./components/SearchBox";
import ResultCard from "./components/ResultCard";
import Skeleton from "./components/Skeleton";
import useDebounce from "./hooks/useDebounce";
import { search, type SearchHit } from "./api";
import "./styles.css";

import SplitText from "./components/SplitText";
import TextType from "./components/TextType";
import AnimatedContent from "./components/AnimatedContent";
import AnimatedList from "./components/AnimatedList";
import LiquidEther from "./components/LiquidEther";

export default function App() {
  const [q, setQ] = useState("");
  const dq = useDebounce(q, 300);
  const [k, setK] = useState(10);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<SearchHit[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function run(qText: string, topk = k) {
    if (!qText.trim()) {
      setResults([]);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      setResults(await search(qText, topk));
    } catch (e: any) {
      setError(e?.message || "Search failed");
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    if (dq) run(dq);
  }, [dq]);

  const handleAnimationComplete = () => {
    console.log("All letters have animated!");
  };

  return (
    <div className="min-h-screen relative bg-gray-50 text-gray-900">
      {/* Cool background */}
      <LiquidEther />

      <Header />

      <main className="mx-auto max-w-4xl px-4 py-10 relative">
        {/* SplitText hero */}
        <SplitText
          text="BM25 Search"
          className="mb-2 block text-center text-4xl font-bold"
          delay={100}
          duration={0.6}
          ease="power3.out"
          splitType="chars"
          from={{ opacity: 0, y: 40 }}
          to={{ opacity: 1, y: 0 }}
          threshold={0.1}
          rootMargin="-100px"
          textAlign="center"
          onLetterAnimationComplete={handleAnimationComplete}
        />

        {/* Typing subtitle */}
        <div className="mb-8 text-center text-gray-600">
          <TextType
            text={["By Rohit Datta"]}
            typingSpeed={75}
            pauseDuration={1500}
            showCursor={true}
            cursorCharacter="|"
          />
        </div>

        {/* Animated content container */}
        <AnimatedContent
          distance={150}
          direction="horizontal"
          reverse={false}
          duration={1.2}
          ease="bounce.out"
          initialOpacity={0.2}
          animateOpacity
          scale={1.02}
          threshold={0.2}
          delay={0.2}
        >
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Search</h2>
            <label className="flex items-center gap-2 text-sm">
              Top-k
              <input
                type="number"
                min={1}
                max={100}
                value={k}
                onChange={(e) => setK(parseInt(e.target.value) || 10)}
                className="w-20 rounded border border-gray-300 px-2 py-1"
              />
            </label>
          </div>

          <SearchBox value={q} setValue={setQ} onSubmit={() => run(q, k)} />
        </AnimatedContent>

        <div className="mt-6 space-y-3">
          {loading &&
            Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} />)}

          {!loading && error && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {!loading && !error && results.length === 0 && q && (
            <div className="text-sm text-gray-500">No results found.</div>
          )}

          {!loading && !error && results.length > 0 && (
            <AnimatedList
              items={results.map((r) => r.title || r.url)}
              onItemSelect={(item, idx) => console.log("selected", idx, item)}
              showGradients={true}
              enableArrowNavigation={true}
              displayScrollbar={true}
            >
              <ul className="space-y-3">
                {results.map((hit) => (
                  <ResultCard
                    key={hit.doc_id + "-" + hit.url}
                    hit={hit}
                    q={q}
                  />
                ))}
              </ul>
            </AnimatedList>
          )}
        </div>
      </main>
    </div>
  );
}
