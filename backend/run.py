import os

import sys

import uvicorn



if __name__ == "__main__":

    # Ensure backend directory is in path

    current_dir = os.path.dirname(os.path.abspath(__file__))

    sys.path.insert(0, current_dir)



    print("=" * 70)

    print("🚀 Starting Secure Collaborative Healthcare Learning System Backend")

    print("=" * 70)

    print("📍 Swagger Documentation: http://localhost:8000/docs")

    print("📍 ReDoc Documentation:   http://localhost:8000/redoc")

    print("📍 Health Endpoint:       http://localhost:8000/health")

    print("=" * 70)



    uvicorn.run(

        "app.main:app",

        host="0.0.0.0",

        port=8000,

        reload=True,

        log_level="info"

    )
