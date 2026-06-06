#!/usr/bin/env python3
"""
Generate comic-style illustrations using OpenAI GPT Image API.
Usage: python3 generate_comic.py "<prompt1>" "<prompt2>" ...
Outputs images to ./comic_output/ directory.

Requires OPENAI_API_KEY environment variable.
"""

import sys
import os
import base64
import time


def generate_comic_panels(prompts, output_dir="comic_output", model="gpt-image-2"):
    """
    Generate comic panel images from text prompts using OpenAI API.

    Args:
        prompts: List of image generation prompts
        output_dir: Directory to save generated images
        model: OpenAI image model to use (default: gpt-image-1)
    """
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL", None),
    )

    os.makedirs(output_dir, exist_ok=True)

    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"Generating panel {i}/{len(prompts)}...")
        print(f"  Prompt: {prompt[:100]}...")

        try:
            response = client.images.generate(
                model=model,
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="b64_json",
            )

            if response.data and len(response.data) > 0:
                image_data = base64.b64decode(response.data[0].b64_json)
                filename = os.path.join(output_dir, f"panel_{i}.png")
                with open(filename, "wb") as f:
                    f.write(image_data)
                print(f"  Saved: {filename}")
                results.append({"panel": i, "prompt": prompt, "file": filename})
            else:
                print(f"  Warning: No image data returned for panel {i}")
                results.append({"panel": i, "prompt": prompt, "error": "No data"})

            # Rate limit: wait between requests
            if i < len(prompts):
                time.sleep(2)

        except Exception as e:
            print(f"  Error generating panel {i}: {e}", file=sys.stderr)
            results.append({"panel": i, "prompt": prompt, "error": str(e)})

    return results


def print_report(results, output_dir):
    """Print a summary report of generated panels."""
    print("\n" + "=" * 50)
    print("Comic Panel Generation Report")
    print("=" * 50)

    success = [r for r in results if "error" not in r]
    failed = [r for r in results if "error" in r]

    print(f"Total panels: {len(results)}")
    print(f"Successful:   {len(success)}")
    print(f"Failed:       {len(failed)}")

    if failed:
        print("\nFailed panels:")
        for r in failed:
            print(f"  Panel {r['panel']}: {r['error']}")

    if success:
        print(f"\nOutput directory: {os.path.abspath(output_dir)}")
        print("Generated files:")
        for r in success:
            print(f"  {r['file']}")

    print("=" * 50)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_comic.py \"<prompt1>\" \"<prompt2>\" ...",
              file=sys.stderr)
        sys.exit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "Error: OPENAI_API_KEY environment variable is not set.\n"
            "Please set it before running:\n"
            "  export OPENAI_API_KEY='your-api-key'\n"
            "Or use a custom endpoint:\n"
            "  export OPENAI_BASE_URL='https://your-proxy-url'\n"
            "  export OPENAI_API_KEY='your-api-key'",
            file=sys.stderr
        )
        sys.exit(1)

    prompts = sys.argv[1:]
    output_dir = "comic_output"

    try:
        results = generate_comic_panels(prompts, output_dir)
        print_report(results, output_dir)

        # Output JSON for programmatic use
        import json
        report_file = os.path.join(output_dir, "report.json")
        with open(report_file, "w") as f:
            json.dump({
                "total": len(results),
                "success": len([r for r in results if "error" not in r]),
                "failed": len([r for r in results if "error" in r]),
                "panels": results,
            }, f, indent=2, ensure_ascii=False)
        print(f"\nJSON report saved to: {report_file}")

    except ImportError:
        print(
            "Error: openai SDK not installed.\n"
            "Install with: pip install openai",
            file=sys.stderr
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
