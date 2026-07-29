import { BrandMark } from "@/components/brand-mark";
import { SignInButton } from "@/components/sign-in-button";
import { oidcConfigured } from "@/lib/auth";
import Link from "next/link";

export default async function SignInPage({ searchParams }: { searchParams: Promise<{ callbackUrl?: string; error?: string }> }) {
  const values = await searchParams;
  const callbackUrl = values.callbackUrl?.startsWith("/") ? values.callbackUrl : "/";
  return <main className="auth-page"><section className="auth-card"><BrandMark /><div><p className="eyebrow">Free public beta</p><h1>Sign in to Lenslayer.</h1><p>Create a workspace and review contracts at no cost during testing. No card, subscription, paid tier, or upgrade prompt.</p></div>{values.error && <p className="auth-alert" role="alert">Your identity provider could not complete this sign-in. Try again or ask your workspace administrator to confirm your access.</p>}<SignInButton callbackUrl={callbackUrl} configured={oidcConfigured} /><Link className="button secondary" href="/sample">Explore a sample review</Link><p className="auth-note">Sessions expire after eight hours. Lenslayer never uses a sign-in to bypass workspace roles.</p></section></main>;
}
