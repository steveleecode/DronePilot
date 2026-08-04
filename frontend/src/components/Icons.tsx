type IconProps = {
  className?: string;
};

export function Loader2({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true">
      <path
        d="M21 12a9 9 0 1 1-6.2-8.55"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="2"
      />
    </svg>
  );
}

export function AlertTriangle({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" aria-hidden="true">
      <path
        d="m12 3 10 18H2L12 3Z"
        fill="none"
        stroke="currentColor"
        strokeLinejoin="round"
        strokeWidth="2"
      />
      <path d="M12 9v5" stroke="currentColor" strokeLinecap="round" strokeWidth="2" />
      <path d="M12 17h.01" stroke="currentColor" strokeLinecap="round" strokeWidth="3" />
    </svg>
  );
}
