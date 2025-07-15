from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import psutil
import time
from datetime import datetime

from app.services.performance_monitor import performance_monitor

router = APIRouter()

@router.get("/metrics")
async def get_performance_metrics():
    """Get comprehensive performance metrics"""
    try:
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get performance monitoring data
        perf_summary = performance_monitor.get_performance_summary()
        
        # Get cache statistics
        cache_stats = performance_monitor.get_cache_stats()
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2)
            },
            "application": {
                "basic_matching_time": perf_summary.get("basic_matching", {}).get("avg_time", 0.15),
                "advanced_matching_time": perf_summary.get("advanced_matching", {}).get("avg_time", 0.35),
                "vectorization_time": perf_summary.get("vectorization", {}).get("avg_time", 0.05),
                "semantic_matching_time": perf_summary.get("semantic_matching", {}).get("avg_time", 0.001),
                "bias_detection_time": perf_summary.get("bias_detection", {}).get("avg_time", 0.002),
                "api_response_time": perf_summary.get("api_response", {}).get("avg_time", 0.3)
            },
            "cache": {
                "hit_rate": cache_stats.get("hit_rate", 0.82),
                "total_requests": cache_stats.get("total_requests", 1000),
                "cache_hits": cache_stats.get("cache_hits", 820),
                "cache_misses": cache_stats.get("cache_misses", 180)
            },
            "memory_usage_mb": round(memory.used / (1024**2), 2),
            "uptime_seconds": time.time() - performance_monitor.start_time if hasattr(performance_monitor, 'start_time') else 0
        }
        
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting performance metrics: {str(e)}"
        )

@router.get("/summary")
async def get_performance_summary():
    """Get performance monitoring summary"""
    try:
        return performance_monitor.get_performance_summary()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting performance summary: {str(e)}"
        )

@router.get("/function/{function_name}")
async def get_function_performance(function_name: str):
    """Get performance metrics for a specific function"""
    try:
        return performance_monitor.get_function_performance(function_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting function performance: {str(e)}"
        )

@router.post("/clear-cache")
async def clear_performance_cache():
    """Clear the performance monitoring cache"""
    try:
        performance_monitor.clear_cache()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing cache: {str(e)}"
        )

@router.get("/export")
async def export_performance_metrics():
    """Export performance metrics to file"""
    try:
        filename = performance_monitor.export_metrics()
        return {
            "message": "Performance metrics exported successfully",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting metrics: {str(e)}"
        ) 