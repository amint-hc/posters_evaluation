import json
import asyncio
import aiofiles
import pandas as pd
from pathlib import Path
from typing import List
from ..models.poster_data import PosterEvaluation, ProcessingLog

class AsyncOutputGenerator:
    """Generate all required output files asynchronously"""
    
    def __init__(self, output_dir: Path, mode: str = "fifteen"):
        self.output_dir = output_dir
        self.mode = mode
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate_master_results(self, evaluations: List[PosterEvaluation]) -> Path:
        """Generate master CSV results file"""
        filename = f"results_master_{self.mode}.csv"
        filepath = self.output_dir / filename
        
        # Prepare data for CSV
        data = []
        for eval in evaluations:
            data.append({
                "Poster File": eval.poster_file,
                "Final Grade": eval.final_grade,
                "Project Number": eval.Q1 if eval.Q1 else "",
                "Project Summary": eval.poster_summary,
                "Evaluation Summary": eval.evaluation_summary
            })
        
        # Create DataFrame and save
        df = pd.DataFrame(data)
        
        # Use asyncio to write file
        csv_content = df.to_csv(index=False)
        async with aiofiles.open(filepath, 'w', encoding='utf-8', newline='') as f:
            await f.write(csv_content.strip())
        
        print(f"Master results saved to: {filepath}")
        return filepath
    
    async def generate_individual_breakdowns(self, evaluations: List[PosterEvaluation]) -> List[Path]:
        """Generate individual JSON breakdown files"""
        breakdown_files = []
        
        async def write_breakdown_file(eval: PosterEvaluation):
            # Determine filename
            if eval.Q1 and eval.Q3:  # Project number and presenter found
                filename = f"{eval.Q1}_{eval.Q3}.json"
            else:
                # Fallback naming
                stem = Path(eval.poster_file).stem
                filename = f"{stem}_Unknown.json"
            
            # Clean filename (remove invalid characters)
            filename = "".join(c for c in filename if c.isalnum() or c in "._-")
            filepath = self.output_dir / filename
            
            # Create JSON data
            json_data = eval.dict()
            
            # Write JSON file asynchronously
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(json_data, indent=2, ensure_ascii=False))
            
            return filepath
        
        # Write all breakdown files concurrently
        tasks = [write_breakdown_file(eval) for eval in evaluations]
        breakdown_files = await asyncio.gather(*tasks)
        
        print(f"Generated {len(breakdown_files)} breakdown files")
        return breakdown_files
    
    async def generate_run_log(self, logs: List[ProcessingLog]) -> Path:
        """Generate JSONL run log file"""
        filepath = self.output_dir / "run_log.jsonl"
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            for log in logs:
                await f.write(log.json() + '\n')
        
        print(f"Run log saved to: {filepath}")
        return filepath
    
    async def generate_all_outputs(self, evaluations: List[PosterEvaluation], 
                                 logs: List[ProcessingLog]) -> dict:
        """Generate all output files concurrently"""
        
        # Run all generation tasks concurrently
        master_task = self.generate_master_results(evaluations)
        breakdown_task = self.generate_individual_breakdowns(evaluations)
        log_task = self.generate_run_log(logs)
        
        master_file, breakdown_files, log_file = await asyncio.gather(
            master_task, breakdown_task, log_task
        )
        
        return {
            "master_file": master_file,
            "breakdown_files": breakdown_files,
            "log_file": log_file
        }
