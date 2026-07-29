import { AlertTriangle, ArrowLeft } from "lucide-react";
import Link from "next/link";
import { BrandMark } from "@/components/brand-mark";

export default async function AuthErrorPage({ searchParams }: { searchParams: Promise<{ error?: string }> }) {
  const { error } = await searchParams;
  const denied = error === "AccessDenied";
  return <main className="auth-page"><section className="auth-card"><BrandMark /><span className="auth-state-icon"><AlertTriangle size={22} /></span><div><p className="eyebrow">{denied ? "Access denied" : "Sign-in interrupted"}</p><h1>{denied ? "This identity does not have workspace access." : "We could not finish signing you in."}</h1><p>{denied ? "Use the email address invited to this workspace or ask an administrator to add your verified work identity." : "Your session was not created. No contract or identity evidence was exposed."}</p></div><Link className="button" href="/signin"><ArrowLeft size={16} />Return to sign in</Link></section></main>;
}
