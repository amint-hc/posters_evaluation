# Testing with Mock Mode

The project includes mock testing capabilities to simulate OpenAI API calls without needing an API key.

## Running in Mock Mode

To start the application in mock mode, run the mock app:

```bash
python -m mock.app
```

## How Mock Mode Works

1. **API Calls are Mocked**: When you upload posters, the mock system:
   - Creates a mock job ID
   - Generates sample results using `generate_mock_results.py`
   - Returns results immediately (no waiting)

2. **Results are Pre-generated**: Results come from mock data that simulates:
   - Different evaluation approaches (direct, reasoning, deep_analysis, strict)
   - Realistic grade distributions
   - Processing logs

3. **File Operations**: You can download Excel files and view results normally

## Testing with Mock Posters

The `mock/posters/` directory contains sample poster images for testing. Upload any images from this folder to test the evaluation workflow.
