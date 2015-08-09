from django.contrib import admin
from gnsite.models import Post
from django.contrib.auth.models import User

# admin registration
admin.site.register(Post)

import random
from datetime import datetime, timedelta

# fixtures & such

def gen_rand_date():
    random_recent_date = datetime.now() - timedelta(random.choice(90))
    return random_recent_date

WORDLIST_PATH = "/usr/share/dict/words"
def gen_rand_text(num_words):
    words = [word.strip() for word in open('/usr/share/dict/words', 'r')]
    random_text = ' '.join([random.choice(words) for i in range(num_words)])
    return random_text

def gen_rand_username_and_email():
    name = (gen_rand_text(1) + random.choice(range(200))) if (random.choice(range(3)) > 2) else gen_rand_text(2).replace(' ', '')
    email = "{0}@emc.com".format(name)
    return (name, email)

def gen_rand_link():
    rand_link = "https://emc.com/gntestlink/{0}".format(
            gen_rand_text(random.randrange(3)).replace(' ', ''))
    return rand_link

def load_fixtures():
    # see whether the fixtures were already loaded
    num_ops = 3
    num_posts_per_op = 5
    if (len(User.objects.all()) > num_ops and
            len(Post.objects.all()) > num_posts_per_op):
        return
    # gen & load 10 users (ops)
    for o in range(num_ops):
        username, email = gen_rand_username_and_email()
        new_op = User.objects.create_user(username, email, username)
        new_op.save()

        # gen & load 30 posts per use
        for p in range(num_posts_per_op):
            new_post = Post(op = new_op,
                    title = gen_rand_text(random.randrange(10)))
            if random.choice(range(2)) > 0:
                new_post.desc = gen_rand_text(random.randrange(50))
            else:
                new_post.link = gen_rand_link()
            new_post.save()

#load_fixtures()
