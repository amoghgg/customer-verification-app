from rest_framework.decorators import api_view
from rest_framework.response import Response
from .sheets import fetch_customer_row


@api_view(['GET'])
def customer_details(request):
    cid = request.GET.get('cid')
    print("🔍 Fetching for CID:", cid)

    if not cid:
        return Response({'error': 'CID not provided'}, status=400)

    row_data = fetch_customer_row(cid)
    print("📦 Row Data Fetched:", row_data)

    if not row_data:
        return Response({
            'cid': cid,
            'name': "Unknown",
            'project': "Unknown",
            'address': "",
            'items': []
        })

    response = {
        'cid': row_data['cid'],
        'name': row_data.get('name', 'Unknown'),
        'project': row_data.get('project', 'Unknown'),
        'address': row_data.get('address', ''),
        'items': row_data.get('items', [])
    }
    return Response(response)


@api_view(['POST'])
def confirm_delivery(request):
    data = request.data
    print("✅ Confirmation Received:", data)
    # You can optionally forward data to a sheet or database here
    return Response({'status': 'Confirmation submitted successfully'})
