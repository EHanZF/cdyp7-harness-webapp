#!/usr/bin/env python3

def summary(title, count):
    print(f"::notice title={title}::{count} violations found")

if __name__ == "__main__":
    # simple smoke run for the formatter
    summary("STATIC_NAMESPACE", 0)
