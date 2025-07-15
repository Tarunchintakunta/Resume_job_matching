#!/usr/bin/env python3
"""
Performance Testing Script for Resume-Job Matching System
Runs comprehensive benchmarks and load tests
"""

import asyncio
import time
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.performance_monitor import performance_monitor, load_tester
from app.services.advanced_matcher import AdvancedResumeMatcher
from app.services.matcher import ResumeMatcher
from app.services.vectorizer import ResumeJobVectorizer
import numpy as np

class PerformanceTestSuite:
    def __init__(self):
        self.results = {}
        self.test_data = self._generate_test_data()
    
    def _generate_test_data(self) -> Dict[str, Any]:
        """Generate test data for performance testing"""
        print("Generating test data...")
        
        # Generate sample resumes
        resumes = []
        for i in range(100):
            resume = {
                "id": f"resume_{i}",
                "name": f"Candidate {i}",
                "skills": ["Python", "JavaScript", "React", "Node.js", "MongoDB"],
                "experience": [{"duration": "3 years", "description": "Software development"}],
                "raw_text": f"Experienced software engineer with skills in Python, JavaScript, React, Node.js, MongoDB. Worked on various projects for {3 + i % 5} years.",
                "vector": np.random.rand(100).tolist()
            }
            resumes.append(resume)
        
        # Generate sample jobs
        jobs = []
        for i in range(20):
            job = {
                "id": f"job_{i}",
                "title": f"Software Engineer {i}",
                "description": f"Looking for a talented software engineer with experience in Python, JavaScript, React, Node.js, MongoDB. {3 + i % 5}+ years experience required.",
                "skills_required": ["Python", "JavaScript", "React", "Node.js", "MongoDB"],
                "requirements": [f"{3 + i % 5}+ years experience", "Bachelor's degree"],
                "vector": np.random.rand(100).tolist()
            }
            jobs.append(job)
        
        return {"resumes": resumes, "jobs": jobs}
    
    @performance_monitor.monitor_performance("basic_matching_benchmark")
    def benchmark_basic_matching(self) -> Dict[str, Any]:
        """Benchmark basic matching algorithm"""
        print("Running basic matching benchmark...")
        
        matcher = ResumeMatcher()
        job = self.test_data["jobs"][0]
        resumes = self.test_data["resumes"]
        
        start_time = time.time()
        results = matcher.rank_resumes(job, resumes)
        end_time = time.time()
        
        return {
            "algorithm": "basic_matching",
            "execution_time": end_time - start_time,
            "resumes_processed": len(resumes),
            "results_count": len(results),
            "avg_score": sum(r["score"] for r in results) / len(results) if results else 0
        }
    
    @performance_monitor.monitor_performance("advanced_matching_benchmark")
    def benchmark_advanced_matching(self) -> Dict[str, Any]:
        """Benchmark advanced matching algorithm"""
        print("Running advanced matching benchmark...")
        
        matcher = AdvancedResumeMatcher()
        job = self.test_data["jobs"][0]
        resumes = self.test_data["resumes"]
        
        start_time = time.time()
        results = matcher.rank_resumes_advanced(job, resumes)
        end_time = time.time()
        
        return {
            "algorithm": "advanced_matching",
            "execution_time": end_time - start_time,
            "resumes_processed": len(resumes),
            "results_count": len(results),
            "avg_score": sum(r["score"] for r in results) / len(results) if results else 0
        }
    
    @performance_monitor.monitor_performance("vectorization_benchmark")
    def benchmark_vectorization(self) -> Dict[str, Any]:
        """Benchmark text vectorization"""
        print("Running vectorization benchmark...")
        
        vectorizer = ResumeJobVectorizer()
        texts = [resume["raw_text"] for resume in self.test_data["resumes"][:50]]
        
        start_time = time.time()
        vectors = []
        for text in texts:
            vector = vectorizer.vectorize(text)
            vectors.append(vector)
        end_time = time.time()
        
        return {
            "algorithm": "vectorization",
            "execution_time": end_time - start_time,
            "texts_processed": len(texts),
            "avg_vector_length": sum(len(v) for v in vectors) / len(vectors) if vectors else 0
        }
    
    @performance_monitor.monitor_performance("semantic_matching_benchmark")
    def benchmark_semantic_matching(self) -> Dict[str, Any]:
        """Benchmark semantic skill matching"""
        print("Running semantic matching benchmark...")
        
        matcher = AdvancedResumeMatcher()
        resume_skills = ["Python", "JavaScript", "React", "Node.js", "MongoDB"]
        job_skills = ["Python", "JS", "React.js", "Node", "MongoDB", "SQL"]
        
        start_time = time.time()
        for _ in range(1000):  # Run 1000 times for benchmark
            result = matcher.semantic_skill_matching(resume_skills, job_skills)
        end_time = time.time()
        
        return {
            "algorithm": "semantic_matching",
            "execution_time": end_time - start_time,
            "iterations": 1000,
            "avg_time_per_iteration": (end_time - start_time) / 1000,
            "match_ratio": result["skills_match_ratio"]
        }
    
    @performance_monitor.monitor_performance("bias_detection_benchmark")
    def benchmark_bias_detection(self) -> Dict[str, Any]:
        """Benchmark bias detection"""
        print("Running bias detection benchmark...")
        
        matcher = AdvancedResumeMatcher()
        test_texts = [
            "He is a senior developer with 10 years of experience.",
            "She is a recent graduate looking for entry-level positions.",
            "The candidate graduated from Harvard University with honors.",
            "We are looking for a talented developer regardless of background."
        ]
        
        start_time = time.time()
        bias_results = []
        for text in test_texts:
            for _ in range(100):  # Run 100 times per text
                result = matcher.detect_bias(text)
                bias_results.append(result)
        end_time = time.time()
        
        return {
            "algorithm": "bias_detection",
            "execution_time": end_time - start_time,
            "texts_processed": len(test_texts) * 100,
            "avg_time_per_text": (end_time - start_time) / (len(test_texts) * 100),
            "bias_detected_count": sum(1 for r in bias_results if r["bias_detected"])
        }
    
    async def run_api_load_tests(self) -> Dict[str, Any]:
        """Run load tests on API endpoints"""
        print("Running API load tests...")
        
        endpoints = [
            ("/api/v1/resumes", "GET"),
            ("/api/v1/jobs", "GET"),
            ("/api/v1/evaluate", "GET")
        ]
        
        load_test_results = {}
        
        for endpoint, method in endpoints:
            print(f"Testing {method} {endpoint}")
            result = await load_tester.run_load_test(
                endpoint=endpoint,
                method=method,
                num_requests=50,
                concurrent=5
            )
            load_test_results[endpoint] = result
        
        return load_test_results
    
    def run_memory_usage_test(self) -> Dict[str, Any]:
        """Test memory usage with large datasets"""
        print("Running memory usage test...")
        
        import psutil
        import gc
        
        # Get initial memory
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Create large dataset
        large_resumes = []
        for i in range(1000):
            resume = {
                "id": f"large_resume_{i}",
                "name": f"Candidate {i}",
                "skills": ["Python", "JavaScript", "React", "Node.js", "MongoDB"] * 10,
                "experience": [{"duration": "5 years", "description": "Software development" * 100}],
                "raw_text": "Experienced software engineer " * 1000,
                "vector": np.random.rand(1000).tolist()
            }
            large_resumes.append(resume)
        
        # Get memory after creating large dataset
        peak_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Run matching on large dataset
        matcher = AdvancedResumeMatcher()
        job = self.test_data["jobs"][0]
        
        start_time = time.time()
        results = matcher.rank_resumes_advanced(job, large_resumes[:100])  # Test with first 100
        end_time = time.time()
        
        # Get final memory
        final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Clean up
        del large_resumes
        gc.collect()
        
        return {
            "test": "memory_usage",
            "initial_memory_mb": initial_memory,
            "peak_memory_mb": peak_memory,
            "final_memory_mb": final_memory,
            "memory_increase_mb": peak_memory - initial_memory,
            "execution_time": end_time - start_time,
            "resumes_processed": 100
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        print("Starting comprehensive performance test suite...")
        
        # Run benchmarks
        self.results["basic_matching"] = self.benchmark_basic_matching()
        self.results["advanced_matching"] = self.benchmark_advanced_matching()
        self.results["vectorization"] = self.benchmark_vectorization()
        self.results["semantic_matching"] = self.benchmark_semantic_matching()
        self.results["bias_detection"] = self.benchmark_bias_detection()
        self.results["memory_usage"] = self.run_memory_usage_test()
        
        # Run load tests
        print("Running load tests...")
        self.results["load_tests"] = asyncio.run(self.run_api_load_tests())
        
        # Get performance summary
        self.results["performance_summary"] = performance_monitor.get_performance_summary()
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate a comprehensive performance report"""
        report = []
        report.append("=" * 80)
        report.append("RESUME-JOB MATCHING SYSTEM PERFORMANCE REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Algorithm Performance
        report.append("ALGORITHM PERFORMANCE")
        report.append("-" * 40)
        
        algorithms = ["basic_matching", "advanced_matching", "vectorization", 
                     "semantic_matching", "bias_detection"]
        
        for algo in algorithms:
            if algo in self.results:
                result = self.results[algo]
                report.append(f"{algo.replace('_', ' ').title()}:")
                report.append(f"  Execution Time: {result['execution_time']:.4f}s")
                if "resumes_processed" in result:
                    report.append(f"  Resumes Processed: {result['resumes_processed']}")
                if "avg_score" in result:
                    report.append(f"  Average Score: {result['avg_score']:.4f}")
                report.append("")
        
        # Memory Usage
        if "memory_usage" in self.results:
            mem = self.results["memory_usage"]
            report.append("MEMORY USAGE")
            report.append("-" * 40)
            report.append(f"Initial Memory: {mem['initial_memory_mb']:.2f} MB")
            report.append(f"Peak Memory: {mem['peak_memory_mb']:.2f} MB")
            report.append(f"Memory Increase: {mem['memory_increase_mb']:.2f} MB")
            report.append("")
        
        # Load Test Results
        if "load_tests" in self.results:
            report.append("LOAD TEST RESULTS")
            report.append("-" * 40)
            for endpoint, result in self.results["load_tests"].items():
                report.append(f"{endpoint}:")
                report.append(f"  Success Rate: {result['success_rate']:.2%}")
                report.append(f"  Requests/Second: {result['requests_per_second']:.2f}")
                report.append(f"  Avg Response Time: {result['execution_time']['mean']:.4f}s")
                report.append("")
        
        # Performance Summary
        if "performance_summary" in self.results:
            summary = self.results["performance_summary"]
            report.append("OVERALL PERFORMANCE SUMMARY")
            report.append("-" * 40)
            report.append(f"Total Function Calls: {summary['total_calls']}")
            report.append(f"Success Rate: {summary['success_rate']:.2%}")
            report.append(f"Average Execution Time: {summary['execution_time']['mean']:.4f}s")
            report.append(f"Cache Hit Rate: {summary['cache_stats']['hit_rate']:.2%}")
            report.append(f"CPU Usage: {summary['system_stats']['cpu_percent']:.1f}%")
            report.append(f"Memory Usage: {summary['system_stats']['memory_percent']:.1f}%")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_results(self, filename: str = None):
        """Save test results to file"""
        if not filename:
            filename = f"performance_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            "test_results": self.results,
            "performance_metrics": performance_monitor.performance_metrics,
            "load_test_results": load_tester.results,
            "generated_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename

def main():
    """Main function to run performance tests"""
    print("Resume-Job Matching System Performance Test Suite")
    print("=" * 60)
    
    # Create test suite
    test_suite = PerformanceTestSuite()
    
    try:
        # Run all tests
        results = test_suite.run_all_tests()
        
        # Generate and print report
        report = test_suite.generate_report()
        print(report)
        
        # Save results
        results_file = test_suite.save_results()
        print(f"\nResults saved to: {results_file}")
        
        # Export performance metrics
        metrics_file = performance_monitor.export_metrics()
        print(f"Performance metrics saved to: {metrics_file}")
        
        # Export load test results
        load_test_file = load_tester.export_results()
        print(f"Load test results saved to: {load_test_file}")
        
    except Exception as e:
        print(f"Error running performance tests: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 