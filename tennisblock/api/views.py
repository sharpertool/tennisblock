from blockdb.models import Season

from .apiutils import JSONResponse, get_current_season as gcs, SeasonSerializer


def get_seasons(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        seasons = Season.objects.all()
        serializer = SeasonSerializer(seasons, many=True)
        return JSONResponse(serializer.data)


def get_current_season(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cs = gcs()
        if cs:
            serializer = SeasonSerializer(cs, many=False)
            return JSONResponse(serializer.data)
        else:
            return "Failed"


def get_latest_buzz(request):
    return JSONResponse([
        {'text': "Block starts September 20th"},
        {'text': "I don't know the holdout dates yet."}
    ])
