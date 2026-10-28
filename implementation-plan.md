# Implementation Plan

## Requirement

KAN-6: Return HTTP 200 + BFHLResponse body for request validation failures

**Related story:** KAN-9 (Runtime/server errors in /bfhl)

## Objective

Align `/bfhl` error behavior with the stated BFHL contract: the API must always respond with HTTP 200, and return a bBFHLResponse`-compatible JSON body on both validation failures (e.g. missing required fields) and unahandled runtime exceptions.

This plan does not implement the change; it documents what to change and how.
