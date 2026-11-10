"""
Comprehensive Performance & Memory Profiler for TRL Debate Engine.
Measures wall-clock latency and Peak Resident Set Size (RSS / Peak Working Set)
including model loading, document ingestion, and deterministic adjudication
on realistic 30-100 page technical PDF documents.
"""

import json
import os
import sys
import time
import threading
from pathlib import Path
from typing import Dict, List, Any
import psutil

# Add package paths
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "packages" / "core" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "document_processing" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "ml_inference" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "competition_engine" / "src"))


class MemorySampler(threading.Thread):
    """Background high-frequency memory sampler to record absolute peak RSS during execution."""

    def __init__(self, interval_sec: float = 0.005):
        super().__init__(daemon=True)
        self.interval_sec = interval_sec
        self.running = True
        self.process = psutil.Process()
        self.peak_rss = self.process.memory_info().rss

    def run(self):
        while self.running:
            try:
                rss = self.process.memory_info().rss
                if rss > self.peak_rss:
                    self.peak_rss = rss
                time.sleep(self.interval_sec)
            except Exception:
                break

    def stop(self) -> int:
        self.running = False
        return self.peak_rss


def profile_single_document(doc_path: Path, run_pipeline_fn) -> Dict[str, Any]:
    """Execute inference on a single document while profiling latency and peak memory."""
    proc = psutil.Process()
    rss_before = proc.memory_info().rss

    sampler = MemorySampler(interval_sec=0.002)
    sampler.start()

    start_time = time.perf_counter()
    assessment = run_pipeline_fn(doc_path, strict_security=False)
    elapsed_sec = time.perf_counter() - start_time

    peak_rss_sampled = sampler.stop()
    rss_after = proc.memory_info().rss
    os_peak_wset = getattr(proc.memory_info(), "peak_wset", peak_rss_sampled)

    return {
        "file_name": doc_path.name,
        "file_size_mb": round(doc_path.stat().st_size / (1024 * 1024), 2),
        "page_count": len(assessment.supporting_evidence) if hasattr(assessment, "page_count") else "N/A",
        "predicted_trl": assessment.predicted_trl,
        "confidence": round(assessment.confidence, 4),
        "latency_sec": round(elapsed_sec, 4),
        "rss_before_mb": round(rss_before / (1024 * 1024), 2),
        "rss_after_mb": round(rss_after / (1024 * 1024), 2),
        "peak_rss_mb": round(max(peak_rss_sampled, os_peak_wset) / (1024 * 1024), 2),
        "rss_delta_mb": round((rss_after - rss_before) / (1024 * 1024), 2),
    }


def run_benchmark():
    proc = psutil.Process()
    initial_rss = proc.memory_info().rss

    print("=" * 80)
    print("TRL DEBATE ENGINE — PERFORMANCE & MEMORY PROFILING")
    print(f"Base Python Process RSS: {initial_rss / (1024 * 1024):.2f} MB")
    print("=" * 80)

    # 1. Measure package import / model load impact
    import_start = time.perf_counter()
    from competition_engine.runner import run_pipeline
    import pypdfium2 as pdfium
    import_time = time.perf_counter() - import_start
    post_import_rss = proc.memory_info().rss

    print(f"Package Import & Pipeline Init Latency: {import_time * 1000:.2f} ms")
    print(f"Post-Import Process RSS: {post_import_rss / (1024 * 1024):.2f} MB")
    print(f"Import Memory Overhead: {(post_import_rss - initial_rss) / (1024 * 1024):.2f} MB")
    print("-" * 80)

    docs_dir = ROOT_DIR / "data" / "sample_evaluation_docs"
    test_files = sorted(docs_dir.glob("*.pdf"))

    if not test_files:
        print(f"No PDF files found in {docs_dir}")
        return

    results = []
    total_start = time.perf_counter()

    for pdf_path in test_files:
        # Determine actual page count via pypdfium2
        pdf_doc = pdfium.PdfDocument(pdf_path)
        page_count = len(pdf_doc)
        del pdf_doc

        print(f"Profiling: {pdf_path.name} ({page_count} pages, {pdf_path.stat().st_size / (1024 * 1024):.2f} MB)...")
        doc_metrics = profile_single_document(pdf_path, run_pipeline)
        doc_metrics["page_count"] = page_count
        results.append(doc_metrics)

        print(
            f"  -> Latency: {doc_metrics['latency_sec']:.3f}s | "
            f"Peak RSS: {doc_metrics['peak_rss_mb']:.2f} MB | "
            f"Predicted TRL: {doc_metrics['predicted_trl']} (Conf: {doc_metrics['confidence']:.2f})"
        )

    total_time = time.perf_counter() - total_start
    final_peak_rss = getattr(proc.memory_info(), "peak_wset", proc.memory_info().rss) / (1024 * 1024)

    print("=" * 80)
    print("SUMMARY PERFORMANCE REPORT")
    print(f"Total Documents Evaluated: {len(results)}")
    print(f"Total Pages Processed:     {sum(r['page_count'] for r in results)}")
    print(f"Total Wall-Clock Time:     {total_time:.3f} s")
    print(f"Average Latency / Doc:     {total_time / len(results):.3f} s")
    print(f"Average Latency / Page:    {(total_time / sum(r['page_count'] for r in results)) * 1000:.2f} ms/page")
    print(f"Overall Peak Process RSS:  {final_peak_rss:.2f} MB")
    print("=" * 80)

    # Save structured report
    report = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "python_version": sys.version,
            "platform": sys.platform,
            "device_cpu_count": psutil.cpu_count(logical=True),
            "baseline_rss_mb": round(initial_rss / (1024 * 1024), 2),
            "post_import_rss_mb": round(post_import_rss / (1024 * 1024), 2),
            "total_documents": len(results),
            "total_pages": sum(r['page_count'] for r in results),
            "total_wall_clock_time_sec": round(total_time, 4),
            "average_latency_per_doc_sec": round(total_time / len(results), 4),
            "overall_peak_process_rss_mb": round(final_peak_rss, 2),
        },
        "per_document_metrics": results
    }

    report_path = ROOT_DIR / "docs" / "performance_benchmark_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved performance report to: {report_path}")


if __name__ == "__main__":
    run_benchmark()
