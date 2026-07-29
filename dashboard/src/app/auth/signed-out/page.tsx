import { ArrowRight, CheckCircle2 } from "lucide-react";
import Link from "next/link";
import { BrandMark } from "@/components/brand-mark";

export default function SignedOutPage() {
  return <main className="auth-page"><section className="auth-card"><BrandMark /><span className="auth-state-icon good"><CheckCircle2 size={22} /></span><div><p className="eyebrow">Session ended</p><h1>You are signed out.</h1><p>This browser no longer has access to the workspace. Shared computers should also be closed when you finish.</p></div><Link className="button" href="/signin">Sign in again<ArrowRight size={16} /></Link></section></main>;
}
