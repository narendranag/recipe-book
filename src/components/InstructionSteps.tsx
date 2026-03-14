export default function InstructionSteps({
  instructions,
}: {
  instructions: string[];
}) {
  return (
    <ol className="space-y-6">
      {instructions.map((step, i) => (
        <li key={i} className="flex gap-4">
          <span className="flex-shrink-0 w-8 h-8 rounded-full bg-accent text-white text-sm font-semibold flex items-center justify-center mt-0.5">
            {i + 1}
          </span>
          <p className="text-sm leading-relaxed text-warm-black pt-1">
            {step}
          </p>
        </li>
      ))}
    </ol>
  );
}
