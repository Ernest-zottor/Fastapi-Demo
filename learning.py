
# the query below returns a dict of Post object and vote. {'Post':{'content}, 'votes':votes}
# So the Pydantic models has to be
# class PostResponse(Basemodel):
#   Post: Post
#   votes: votes





# results = db.query(models.Post, func.count(models.Votes.post_id).label('votes')).join(models.Votes, models.Votes.post_id==models.Post.id, isouter=True).group_by(models.Post.id).all()
    
# formatted_results = []
# for post, votes in results:
#     formatted_results.append({'post':{
#         'id': post.id,
#         'title': post.title,
#         'content': post.content,
#         'user_id': post.user_id,
#         'created_at': post.created_at,
#         'published': post.published,
#         'owner': post.owner,
        
#     }, 
#     'votes': votes})