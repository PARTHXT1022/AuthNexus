# AuthNexus

A from-scratch implementation of OAuth2 and OpenID Connect (OIDC), built as
a learning project to understand authentication and authorization at a
mechanical level, rather than relying on a library as a black box.

## What this is

This repo implements a working identity provider that issues and validates
its own tokens — including JWT signing with RSA keys, the Authorization
Code flow with PKCE, and refresh token rotation. The eventual goal is to
use this as the authentication layer for a multi-tenant Model Context
Protocol (MCP) server, where an LLM-based client can query SaaS account
metrics while the server enforces that each caller only ever accesses data
for the tenant they're authorized for.

## Why

Most OAuth2/OIDC integration work treats the protocol as something you
configure, not something you understand. Building the identity provider
itself — token signing, PKCE, discovery, rotation — makes the security
guarantees something you can reason about directly, which matters
especially when the eventual client making requests is an LLM rather than
a predictable, hand-written application.

## Status

The identity provider (OAuth2/OIDC core) is implemented and functional.
The MCP server, tenant-scoping logic, and MCP client integration are in
progress.

## Running it

```bash
uv sync
uv run fastapi dev
```

Interactive API docs available at `/docs` once running.