# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Requests,Votes,Discussion
#from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django import forms
from django.forms import ModelForm,Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def vote(request):
    if request.user.is_authenticated():
        if request.method == 'POST':

            reqids = request.POST.getlist('requestid')
            scores = request.POST.getlist('score')
            newvote = request.POST.get('newvote')
            if newvote:
                votebyuser = Votes.objects.create(user=request.user)
            else:
                votebyuser = Votes.objects.get(user=request.user)
            for i,score in enumerate(scores):
    
                wwrequest = Requests.objects.get(id=reqids[i])
                votebyuser.rank1.remove(wwrequest)
                votebyuser.rank2.remove(wwrequest)
                votebyuser.rank3.remove(wwrequest)
                votebyuser.rank4.remove(wwrequest)
                votebyuser.rank5.remove(wwrequest)
                if score=='1':
                    votebyuser.rank1.add(wwrequest)
                elif score=='2':
                    votebyuser.rank2.add(wwrequest)
                elif score=='3':
                    votebyuser.rank3.add(wwrequest)
                elif score=='4':
                    votebyuser.rank4.add(wwrequest)
                elif score=='5':
                    votebyuser.rank5.add(wwrequest)
            
            return HttpResponseRedirect('/wwrequests/viewVotes')
        else:
            query = Requests.objects.order_by('-pub_date')
            try:
                votes = Votes.objects.get(user=request.user)
                requests_list=''
                for i,q in enumerate(query):
                    selected = ['','','','','','']
                    if q in votes.rank1.all():
                        selected[1]='selected'
                    elif q in votes.rank2.all():
                        selected[2]='selected'
                    elif q in votes.rank3.all():
                        selected[3]='selected'
                    elif q in votes.rank4.all():
                        selected[4]='selected'
                    elif q in votes.rank5.all():
                        selected[5]='selected'
                    requests_list +='<tr>'
                    requests_list +='<td>'+q.Request+'</td>'
                    requests_list +='<td>'+q.Remark+'</td>'
                    requests_list +='<td>'+q.From.username+'</td>'
                    requests_list +='<td>'
                    requests_list +="<select type='submit' name='score'>"
                    requests_list +='<option value=0 '+selected[0]+'>_</option>'
                    requests_list +='<option value=1 '+selected[1]+'>1</option>'
                    requests_list +='<option value=2 '+selected[2]+'>2</option>'
                    requests_list +='<option value=3 '+selected[3]+'>3</option>'
                    requests_list +='<option value=4 '+selected[4]+'>4</option>'
                    requests_list +='<option value=5 '+selected[5]+'>5</option>'
                    requests_list +='</select>'
                    requests_list +="<input type='hidden' name='requestid' value='"+str(q.id)+"'/>"
                    #requests_list +="<input type='hidden' name='newvote' value=0/>"
                    requests_list +='</td>'
                    requests_list +='</tr>'


                context = {'new_or_update':'(update vote)',
                           'requests_list':requests_list,
                           }
                return render(request,'wwrequests/vote.html',context)
            except Votes.DoesNotExist:
                requests_list=''
                for i,q in enumerate(query):
                    requests_list +='<tr>'
                    requests_list +='<td>'+q.Request+'</td>'
                    requests_list +='<td>'+q.Remark+'</td>'
                    requests_list +='<td>'+q.From.username+'</td>'
                    requests_list +='<td>'
                    requests_list +="<select type='submit' name='score'>"
                    requests_list +='<option value=0>_</option>'
                    requests_list +='<option value=1>1</option>'
                    requests_list +='<option value=2>2</option>'
                    requests_list +='<option value=3>3</option>'
                    requests_list +='<option value=4>4</option>'
                    requests_list +='<option value=5>5</option>'
                    requests_list +='</select>'
                    requests_list +="<input type='hidden' name='requestid' value='"+str(q.id)+"'/>"
                    requests_list +="<input type='hidden' name='newvote' value=1/>"
                    requests_list +='</td>'
                    requests_list +='</tr>'


                context = {'new_or_update':'(new vote)',
                           'requests_list':requests_list,
                           }
                return render(request,'wwrequests/vote.html',context)
    else:
        return HttpResponseRedirect(reverse('login'))
            
def view(request):
    #if user is not None:
    if request.user.is_authenticated():
        """Return all requests"""
        query = Requests.objects.order_by('-pub_date')
     
        context = {'requests_list':query}
        return render(request,'wwrequests/index.html',context)
    else:
        return HttpResponseRedirect(reverse('login'))
def discuss_detail(request,reqid):
    #if user is not None:
    if request.user.is_authenticated():
        if request.method == 'POST':
            dis_content = request.POST.get('discussion')
            if dis_content:
                try:
                    Discussion.objects.get(content=dis_content,user=request.user)
                except(Discussion.DoesNotExist):
                    Discussion.objects.create(content=dis_content,
                                          request=Requests.objects.get(id=reqid),
                                          user=request.user
                                          )

        req = Requests.objects.get(id=reqid)

        table_list ='<tr>'
        table_list+='<th>Category</th>'
        table_list+='<th>Request</th>'
        table_list+='<th>Remark</th>'
        table_list+='<th>From</th>'
        table_list+='<th>Reference</th>'
        table_list+='<th>Schedule</th>'
        table_list+='<th>Status</th>'
        table_list+='<th>Comment</th>'
        table_list+='</tr>'
        table_list+='<tr>'
        table_list+='<td>'+req.Category+'</td>'
        table_list+='<td>'+req.Request+'</td>'
        table_list+='<td>'+req.Remark+'</td>'
        table_list+='<td>'+req.From.username+'</td>'
        table_list+='<td>'+req.Reference+'</td>'
        table_list+='<td>'+req.Schedule+'</td>'
        table_list+='<td>'+req.Status+'</td>'
        table_list+='<td>'+req.Comment+'</td>'
        table_list+='</tr>'
        
        discussion_list = []
        for d in req.discussion_set.all():
            discussion_list.append([d.user.username,d.content])
        context = {'table_list':table_list,
                   'discussion_list':discussion_list}
        return render(request,'wwrequests/discuss_detail.html',context)
    else:
        return HttpResponseRedirect(reverse('login'))
def edit_req(request,reqid):
    #if user is not None:
    if request.user.is_authenticated():
        req = Requests.objects.get(id=reqid)
        if request.method == 'POST':
            rf = RequestsForm(request.POST,instance=req)
            if rf.is_valid():
                rf.save()
                return HttpResponseRedirect('/wwrequests')
            else:
                return HttpResponse("update request fail!! <a href='/'>try agian</a>")
        else:
            
            rf = RequestsForm(instance=req)
            return render_to_response('wwrequests/Edit.html',{'edit':rf}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('login'))
def del_req(request,reqid):
    #if user is not None:
    if request.user.is_authenticated():
        if request.method == 'POST':
            Requests.objects.get(id=reqid).delete()
            context = {'deleted':'The request has been deleted.'}
        else:
            req = Requests.objects.get(id=reqid)

            table_list ='<tr>'
            table_list+='<th>Category</th>'
            table_list+='<th>Request</th>'
            table_list+='<th>Remark</th>'
            table_list+='<th>From</th>'
            table_list+='<th>Reference</th>'
            table_list+='<th>Schedule</th>'
            table_list+='<th>Status</th>'
            table_list+='<th>Comment</th>'
            table_list+='</tr>'
            table_list+='<tr>'
            table_list+='<td>'+req.Category+'</td>'
            table_list+='<td>'+req.Request+'</td>'
            table_list+='<td>'+req.Remark+'</td>'
            table_list+='<td>'+req.From.username+'</td>'
            table_list+='<td>'+req.Reference+'</td>'
            table_list+='<td>'+req.Schedule+'</td>'
            table_list+='<td>'+req.Status+'</td>'
            table_list+='<td>'+req.Comment+'</td>'
            table_list+='</tr>'
            context = {'to_confirm':table_list}
        return render(request,'wwrequests/Delete.html',context)
    else:
        return HttpResponseRedirect(reverse('login'))
def view_votes(request):
    #if user is not None:
    if request.user.is_authenticated():
        """show votes by all users"""
        if Votes.objects.count() == 0:
            return HttpResponse("no votes yet! <a href='/'>view list>></a>")
        votes = Votes.objects.all()
        if votes:#votes exist
            Requests.objects.all().update(total_score=0)
            for v in votes:
                for req in v.rank1.all():
                    req.total_score+=1
                    req.save()
                for req in v.rank2.all():
                    req.total_score+=2
                    req.save()
                for req in v.rank3.all():
                    req.total_score+=3
                    req.save()
                for req in v.rank4.all():
                    req.total_score+=4
                    req.save()
                for req in v.rank5.all():
                    req.total_score+=5
                    req.save()
            
            fm = "<tr>"
            fm+= "<th>Requests</th><th>Tot.Score</th>"
            query = Requests.objects.order_by('total_score')
            votes = Votes.objects.all()
            for v in votes:
                name = v.user.username
                fm+= "<th><u title='"+name+"'>"+name[0]+"</th>"
            fm+= "</th>"
            for q in query:
                fm+= "<tr>"
                fm+= "<td>"+q.Request+"</td>"
                fm+= "<td>"+str(q.total_score)+"</td>"
                
                for v in votes:
                    rank=''
                    if q in v.rank1.all():
                        rank='1'
                    elif q in v.rank2.all():
                        rank='2'
                    elif q in v.rank3.all():
                        rank='3'
                    elif q in v.rank4.all():
                        rank='4'
                    elif q in v.rank5.all():
                        rank='5'
                    fm+= "<td>"+rank+"</td>"
                fm+= "</tr>"
                    
            context = {'fm':fm}
            return render(request,'wwrequests/ListVotes.html',context)
    else:
        return HttpResponseRedirect(reverse('login'))

def regist(req):
        if req.method == 'POST':
            uf = UserCreationForm(req.POST)
            if uf.is_valid():
                uf.save()
                return HttpResponse("regist success! <a href='/login'>login>></a>")
            else:
                return HttpResponse("regist fail! <a href='/regist'>regist again>></a>")
        else:
            uf = UserCreationForm()
            return render_to_response('registration/regis.html',{'uf':uf}, context_instance=RequestContext(req))
        
class RequestsForm(ModelForm):
    class Meta:
        model = Requests
        fields = ['Type','Category','Request','Remark','From']
        widgets = {
            'Type':Select(choices=(
                ('HardwareA','HardwareA'),
                ('HardwareB','HardwareB'),
                ('Software','Software'),))
            }

def addWWRequest(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            rf = RequestsForm(request.POST)

            if rf.is_valid():
                rf.save()
                return HttpResponseRedirect('/wwrequests')
            else:
                return HttpResponse("add request fail!! <a href='addRequest'>try agian</a>")
        else:
            rf = RequestsForm(initial={'From':request.user})
            return render_to_response('wwrequests/addRequest.html',{'new_request':rf}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('login'))

def uploadXLS(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            req_Type      = request.POST.getlist('Type')
            req_Category  = request.POST.getlist('Category')
            req_Request   = request.POST.getlist('Request')
            req_Remark    = request.POST.getlist('Remark')
            req_From      = request.POST.getlist('From')
            req_Reference = request.POST.getlist('Reference')
            req_Schedule  = request.POST.getlist('Schedule')
            req_Status    = request.POST.getlist('Status')
            req_Comment   = request.POST.getlist('Comment')

            err = ''
            for i,r in enumerate(req_Request):
                if req_From[i]=='':
                    req_From[i]='unknown'
                try:
                    User.objects.get(username=req_From[i])
                except User.DoesNotExist:
                    user=User.objects.create_user(req_From[i],'unknown@nikon.com','a')
                    user.save()
                try:   
                    Requests.objects.create(Type=req_Type[i],
                                            Category=req_Category[i],
                                            Request=req_Request[i],
                                            Remark=req_Remark[i],
                                            From=User.objects.get(username=req_From[i]),
                                            Reference=req_Reference[i],
                                            Schedule=req_Schedule[i],
                                            Status=req_Status[i],
                                            Comment=req_Comment[i])
                except IntegrityError:
                    err+='<br/>'+req_Request[i]+'<br/>'
            if err == '':
                return HttpResponseRedirect('/wwrequests')
            else:
                return HttpResponse('<h1>The following items already exist:</h1>'+err)
        else:
            return render_to_response('wwrequests/uploadRequestsByIE.html',context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('login'))
def downloadXLS(request):
    if request.user.is_authenticated():
        req_all =  Requests.objects.all()
        if req_all.count >0:
            table_list ='<tr>'
            table_list+='<th>Category</th>'
            table_list+='<th>Request</th>'
            table_list+='<th>Remark</th>'
            table_list+='<th>From</th>'
            table_list+='<th>Reference</th>'
            table_list+='<th>Schedule</th>'
            table_list+='<th>Status</th>'
            table_list+='<th>Comment</th>'
            table_list+='</tr>'
            table_list+='<tr>'
            for req in req_all:
                table_list+='<td>'+req.Category+'</td>'
                table_list+='<td>'+req.Request+'</td>'
                table_list+='<td>'+req.Remark+'</td>'
                table_list+='<td>'+req.From.username+'</td>'
                table_list+='<td>'+req.Reference+'</td>'
                table_list+='<td>'+req.Schedule+'</td>'
                table_list+='<td>'+req.Status+'</td>'
                table_list+='<td>'+req.Comment+'</td>'
                table_list+='</tr>'
            context = {'request_list':table_list}
            return render(request,'wwrequests/downloadXLSByIE.html',context)
        else:
            return HttpResponse('<h1>The following items already exist:</h1>'+err)
    else:
        return HttpResponseRedirect(reverse('login'))
