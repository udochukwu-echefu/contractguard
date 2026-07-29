"use client";

import { LogOut } from "lucide-react";
import { signOut } from "next-auth/react";
import { BrandMark } from "@/components/brand-mark";

export default function SignOutPage() {
  return <main className="auth-page"><section className="auth-card"><BrandMark /><div><p className="eyebrow">End secure session</p><h1>Sign out of Lenslayer?</h1><p>Signing out removes this browser session. It does not change your workspace membership or audit history.</p></div><button className="button" type="button" onClick={() => signOut({ callbackUrl: "/auth/signed-out" })}><LogOut size={16} />Sign out</button></section></main>;
}
