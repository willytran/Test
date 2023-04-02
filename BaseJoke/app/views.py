from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django import forms

quotes = {
    '1': {
        'id': 1,
        'text': 'Why did the tomato turn red? Because it saw the salad dressing!',
        'author': 'Anna'
    }
}
verified_authors = [('Anna Smith', 'Anna Smith'), ('John Doe', 'John Doe'), ('Jane Smith', 'Jane Smith')]

class QuoteForm(forms.Form):
    quote = forms.CharField(label='Quote', max_length=120, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    author = forms.ChoiceField(choices=verified_authors, widget=forms.Select(attrs={'class': 'form-control'}))



# index page displaying all entries
def index(request):
    rendered = render(request, 'app/index.html', {'quotes': quotes.values()})
    highlight = request.GET.get('highlight')
    try:
        highlight = int(highlight)
    except: 
        highlight = None
    
    return render(request, 'app/index.html', {
        'quotes': quotes.values(),
        'highlight': highlight
    })

# page for adding new entries
def add(request):
    global id

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            id = len(quotes) + 1
            quotes[id] = {
                'id': id,
                'text': form.cleaned_data['quote'],
                'author': form.cleaned_data['author']
            }
            
            # add GET request parameter to highlight correct quote
            response = redirect('app:index')
            response['Location'] += f'?highlight={id}'
            return response
    else:
        form = QuoteForm()

    return render(request, 'app/add.html', { 'form': form })

# get JSON version of an entry
def get_user_entry(request, id):
    entry = quotes.get(id)
    if entry is None:
        return JsonResponse({'error': 'Entry does not exist'}, status=404)
    else:
        return JsonResponse(entry)