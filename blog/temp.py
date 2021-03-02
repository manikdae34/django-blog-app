        # for que in query.split():
        #     print('searching for ', que)
        #     poslist = Post.objects.filter(
        #         Q(title__icontains=que) | Q(description__icontains=que) | Q(tags__icontains=que)
        #     )
        #     print(len(poslist))
        #     post_list.extend(poslist)
        #     print(post_list)
        # print('final list =', post_list)