# Create your views here.

from blockdb.models import Season

from .apiutils import JSONResponse, get_current_season, SeasonSerializer

def getSeasons(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        seasons = Season.objects.all()
        serializer = SeasonSerializer(seasons, many=True)
        return JSONResponse(serializer.data)

def getCurrentSeason(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cs = get_current_season()
        if cs:
            serializer = SeasonSerializer(cs, many=False)
            return JSONResponse(serializer.data)
        else:
            return "Failed"

def getCurrentSeasonDates(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cs = get_current_season()
        if cs:
            startDate = cs.startdate
            endDate = cs.enddate

            return 'Nice'

    return 'Failure'

def getLatestBuzz(request):

    return JSONResponse([
        {'text': "Block starts September 20th"},
        {'text': "I don't know the holdout dates yet."}
    ])


