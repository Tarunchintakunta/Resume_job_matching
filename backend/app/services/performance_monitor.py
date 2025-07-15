import time
import psutil
import threading
from typing import Dict, List, Any, Optional
from functools import wraps
import json
import os
from datetime import datetime
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed

class PerformanceMonitor:
    def __init__(self, cache_enabled: bool = True, max_cache_size: int = 1000):
        self.cache_enabled = cache_enabled
        self.max_cache_size = max_cache_size
        self.cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
        self.performance_metrics = []
        self.lock = threading.Lock()
    
    def monitor_performance(self, func_name: str = None):
        """Decorator to monitor function performance"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                except Exception as e:
                    success = False
                    raise e
                finally:
                    end_time = time.time()
                    end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
                    
                    execution_time = end_time - start_time
                    memory_used = end_memory - start_memory
                    
                    metric = {
                        "function": func_name or func.__name__,
                        "execution_time": execution_time,
                        "memory_used_mb": memory_used,
                        "timestamp": datetime.now().isoformat(),
                        "success": success,
                        "cpu_percent": psutil.cpu_percent(),
                        "memory_percent": psutil.virtual_memory().percent
                    }
                    
                    with self.lock:
                        self.performance_metrics.append(metric)
                    
                    # Keep only last 1000 metrics
                    if len(self.performance_metrics) > 1000:
                        self.performance_metrics = self.performance_metrics[-1000:]
                
                return result
            return wrapper
        return decorator
    
    def cache_result(self, key: str, ttl: int = 3600):
        """Decorator to cache function results"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.cache_enabled:
                    return func(*args, **kwargs)
                
                # Create cache key
                cache_key = f"{key}:{hash(str(args) + str(sorted(kwargs.items())))}"
                
                # Check cache
                if cache_key in self.cache:
                    cache_entry = self.cache[cache_key]
                    if time.time() - cache_entry["timestamp"] < ttl:
                        self.cache_hits += 1
                        return cache_entry["result"]
                
                # Cache miss
                self.cache_misses += 1
                result = func(*args, **kwargs)
                
                # Store in cache
                with self.lock:
                    if len(self.cache) >= self.max_cache_size:
                        # Remove oldest entry
                        oldest_key = min(self.cache.keys(), 
                                       key=lambda k: self.cache[k]["timestamp"])
                        del self.cache[oldest_key]
                    
                    self.cache[cache_key] = {
                        "result": result,
                        "timestamp": time.time()
                    }
                
                return result
            return wrapper
        return decorator
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics"""
        if not self.performance_metrics:
            return {"message": "No performance data available"}
        
        execution_times = [m["execution_time"] for m in self.performance_metrics]
        memory_usage = [m["memory_used_mb"] for m in self.performance_metrics]
        
        return {
            "total_calls": len(self.performance_metrics),
            "success_rate": sum(1 for m in self.performance_metrics if m["success"]) / len(self.performance_metrics),
            "execution_time": {
                "mean": sum(execution_times) / len(execution_times),
                "median": sorted(execution_times)[len(execution_times) // 2],
                "min": min(execution_times),
                "max": max(execution_times),
                "p95": sorted(execution_times)[int(len(execution_times) * 0.95)]
            },
            "memory_usage": {
                "mean_mb": sum(memory_usage) / len(memory_usage),
                "max_mb": max(memory_usage),
                "total_mb": sum(memory_usage)
            },
            "cache_stats": {
                "hits": self.cache_hits,
                "misses": self.cache_misses,
                "hit_rate": self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0,
                "cache_size": len(self.cache)
            },
            "system_stats": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage_percent": psutil.disk_usage('/').percent
            }
        }
    
    def get_function_performance(self, function_name: str) -> Dict[str, Any]:
        """Get performance metrics for a specific function"""
        function_metrics = [m for m in self.performance_metrics if m["function"] == function_name]
        
        if not function_metrics:
            return {"message": f"No data for function {function_name}"}
        
        execution_times = [m["execution_time"] for m in function_metrics]
        
        return {
            "function": function_name,
            "total_calls": len(function_metrics),
            "success_rate": sum(1 for m in function_metrics if m["success"]) / len(function_metrics),
            "execution_time": {
                "mean": sum(execution_times) / len(execution_times),
                "median": sorted(execution_times)[len(execution_times) // 2],
                "min": min(execution_times),
                "max": max(execution_times),
                "p95": sorted(execution_times)[int(len(execution_times) * 0.95)]
            },
            "recent_calls": function_metrics[-10:]  # Last 10 calls
        }
    
    def clear_cache(self):
        """Clear the cache"""
        with self.lock:
            self.cache.clear()
            self.cache_hits = 0
            self.cache_misses = 0
    
    def export_metrics(self, filename: str = None):
        """Export performance metrics to JSON file"""
        if not filename:
            filename = f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            "summary": self.get_performance_summary(),
            "metrics": self.performance_metrics,
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename

class LoadTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
    
    async def test_endpoint(self, endpoint: str, method: str = "GET", 
                          data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                if method.upper() == "GET":
                    async with session.get(url, headers=headers) as response:
                        response_text = await response.text()
                        success = response.status == 200
                elif method.upper() == "POST":
                    async with session.post(url, json=data, headers=headers) as response:
                        response_text = await response.text()
                        success = response.status in [200, 201]
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                return {
                    "endpoint": endpoint,
                    "method": method,
                    "success": success,
                    "status_code": response.status,
                    "execution_time": execution_time,
                    "response_size": len(response_text),
                    "timestamp": datetime.now().isoformat()
                }
        
        except Exception as e:
            end_time = time.time()
            return {
                "endpoint": endpoint,
                "method": method,
                "success": False,
                "error": str(e),
                "execution_time": end_time - start_time,
                "timestamp": datetime.now().isoformat()
            }
    
    async def run_load_test(self, endpoint: str, method: str = "GET", 
                          data: Dict = None, headers: Dict = None,
                          num_requests: int = 100, concurrent: int = 10) -> Dict[str, Any]:
        """Run load test on an endpoint"""
        print(f"Running load test: {num_requests} requests, {concurrent} concurrent")
        
        semaphore = asyncio.Semaphore(concurrent)
        
        async def make_request():
            async with semaphore:
                return await self.test_endpoint(endpoint, method, data, headers)
        
        # Create tasks
        tasks = [make_request() for _ in range(num_requests)]
        
        # Execute all requests
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        # Process results
        successful_requests = [r for r in results if isinstance(r, dict) and r.get("success")]
        failed_requests = [r for r in results if isinstance(r, dict) and not r.get("success")]
        
        execution_times = [r["execution_time"] for r in successful_requests]
        
        test_summary = {
            "endpoint": endpoint,
            "method": method,
            "total_requests": num_requests,
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / num_requests,
            "total_time": end_time - start_time,
            "requests_per_second": num_requests / (end_time - start_time),
            "execution_time": {
                "mean": sum(execution_times) / len(execution_times) if execution_times else 0,
                "median": sorted(execution_times)[len(execution_times) // 2] if execution_times else 0,
                "min": min(execution_times) if execution_times else 0,
                "max": max(execution_times) if execution_times else 0,
                "p95": sorted(execution_times)[int(len(execution_times) * 0.95)] if execution_times else 0
            },
            "errors": [r.get("error") for r in failed_requests if r.get("error")],
            "timestamp": datetime.now().isoformat()
        }
        
        self.results.append(test_summary)
        return test_summary
    
    def get_load_test_summary(self) -> Dict[str, Any]:
        """Get summary of all load tests"""
        if not self.results:
            return {"message": "No load test results available"}
        
        return {
            "total_tests": len(self.results),
            "average_success_rate": sum(r["success_rate"] for r in self.results) / len(self.results),
            "average_rps": sum(r["requests_per_second"] for r in self.results) / len(self.results),
            "tests": self.results
        }
    
    def export_results(self, filename: str = None):
        """Export load test results to JSON file"""
        if not filename:
            filename = f"load_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            "summary": self.get_load_test_summary(),
            "results": self.results,
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename

# Global performance monitor instance
performance_monitor = PerformanceMonitor()
load_tester = LoadTester() 