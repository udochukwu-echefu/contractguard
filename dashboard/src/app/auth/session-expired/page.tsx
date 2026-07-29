import { ArrowRight, Clock3 } from "lucide-react";
import Link from "next/link";
import { BrandMark } from "@/components/brand-mark";

export default function SessionExpiredPage() {
  return <main className="auth-page"><section className="auth-card"><BrandMark /><span className="auth-state-icon"><Clock3 size={22} /></span><div><p className="eyebrow">Session expired</p><h1>Verify your identity again.</h1><p>Lenslayer sessions expire after eight hours. Your unsent changes were not submitted to the workspace.</p></div><Link className="button" href="/signin">Continue to sign in<ArrowRight size={16} /></Link></section></main>;
}
