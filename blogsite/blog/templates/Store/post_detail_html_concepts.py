{%  extends 'blog/base.html'  %}

{% block body_block %}
    <br>

    <div class="container">


        {% if user.is_authenticated %}
              {% if post.author_id == user.id %}

                      <p>
                          <table
                            <tr>
                              <td><a class="btn btn-warning" href="{% url 'blog:post_edit' pk=post.pk %}">Update</a></td>
                              <td>&nbsp;</td>
                              <td>&nbsp;</td>
                              <td><a class="btn btn-danger" href="{% url 'blog:post_remove' pk=post.pk %}">Delete</a></td>
                            </tr>
                          </table>

                      </p>
              {% endif %}

              <div class="bgi">
                <br>
                {% if post.published_date %}
                    <time class="date">
                        {{ post.published_date }}

                    </time>
                {% endif %}
                <br>
                <br>
                <h2>{{ post.title }}</h2>
                {% if post.header_image %}
                    <img src="{{ post.header_image.url }}" alt="">
                {% endif %}

                <p>{{ post.text|safe}}</p>

                {% if post.author.first_name and post.author.last_name %}
                    <h5>By {{post.author.first_name}} {{post.author.last_name}}</h5>
                {% else %}
                    <h5 >By {{post.author.username}}</h5>
                {% endif %}

                <!-- By {{post.author}} -->
                <!-- here post is a context object name from PostDetailView  which can access all fields of Post model (e.g. post.text) and then we are connectig it with it's field i.e. author -->

                <!-- By {{post.author.first_name}} {{post.author.last_name}} -->
                <!-- {{post.author.username}} -->
                <!-- here post is a context object name from PostDetailView  which can access all fields of Post model (e.g. post.text) and then we are connectig it with it's field i.e. author which is also an obj of Class User and so author can access fields of Class User i.e. username -->
                <!-- This is the way we connect different fields in different tables(Models) to get desired columns'(fields) row(data)-->
                <br><br>
                <div class="card mb-3">
                  <div class="row g-0">
                    <div class="col-md-2">
                      {% if post.author.profile.profile_pic %}
                          <img src="{{post.author.profile.profile_pic.url}}" class="img-fluid rounded-start" alt="...">
                      {% endif %}
                    </div>
                    <div class="col-md-10">
                      <div class="card-body">
                        {% if post.author.first_name and post.author.last_name %}
                            <h5 class="card-title">{{post.author.first_name}} {{post.author.last_name}}</h5>
                        {% else %}
                            <h5 class="card-title">{{post.author.username}}</h5>
                        {% endif %}

                        <p class="small text-muted">
                              {% if post.author.profile.id %}
                                    <a href="{% url 'blog:show_profile_page' post.author.profile.id %}">Profile Page</a> |
                              {% endif %}

                              {% if post.author.profile.fb_url %}
                                <a href="{{post.author.profile.fb_url}}">Facebook </a> |
                             {% endif %}
                             {% if post.author.profile.pratilipi_url%}
                                <a href="{{post.author.profile.pratilipi_url}}">Pratilipi </a> |
                             {% endif %}
                             {% if post.author.profile.linkedin_url %}
                                <a href="{{post.author.profile.linkedin_url}}">Linked In</a>
                             {% endif %}
                        </p>
                        <p class="card-text">{{post.author.profile.bio}}</p>

                      </div>
                    </div>
                  </div>
                </div>






                  <!-- why we have used post.author before profile.profile_pic.url , because we are calling everything here by using post/post.author as far as Post model's items(fields)and User model's items(fields) are concerned respectively.this is very IMP. CONCEPT.-->
                  <!-- This is the way we connect different fields in different tables(Models) to get desired columns'(fields) row(data)-->
                <!-- <a href="{% url 'blog:show_profile_page' post.author.profile.id %}">Show Profile Page</a> -->
                <!-- why we have used post.author before profile.id , because we are calling everything here by using post/post.author as far as Post model's items(fields)and User model's items(fields) are concerned respectively.this is very IMP. CONCEPT.-->


                <br><br>
                <img src="https://th.bing.com/th/id/R.3a8d60d51eb12e18fa6e25ef6b9d7037?rik=MyMHO%2fUHOsM%2b%2fw&riu=http%3a%2f%2fpngimg.com%2fuploads%2flike%2flike_PNG10.png&ehk=VYgcKJIzr9mN1c%2bX23n%2bM1hGyEZ2PMf9BGzeJhYZOl0%3d&risl=&pid=ImgRaw" width="2%" height="2%" alt=""> {{ total_likes }}
                <hr>
                <form action="{% url 'blog:like_post' pk=post.pk %}" method="post">
                  {% csrf_token %}
                  <button type="submit" name="post_id"  value="{{post.id}}" class="btn btn-primary btn-sm">Like</button>
                  <!-- here we are passing the id of post which is being liked !-->
                </form>
                <br><br><br>









              </div>
              <br>
               {% if not post.author_id == user.id %}
                  <p><a class="btn btn-success" href="{% url 'blog:add_comment_to_post' pk=post.pk %}">Add Comment</a></p>
               {% endif %}

              <hr>
              {% for comment in post.comments.all %}
                    {% if comment.approved_comment or user.is_authenticated %}

                          {% if not comment.approved_comment %}
                          <p>
                            <table>
                            <tr>
                              <td><a  href="{% url 'blog:comment_approve' pk=comment.pk %}">✅</a></td>
                              <td>&nbsp;</td>
                              <td>&nbsp;</td>
                              <td><a href="{% url 'blog:comment_remove' pk=comment.pk %}">❌</a></td>
                            </tr>
                          </table>
                          </p>
                          {% endif %}
                        <div class="date">{{ comment.created_date }}</div>
                        <strong>{{ comment.author }} said,</strong>
                        <p>{{ comment.text|linebreaks }}</p>

                        <hr>


                    {% endif %}
                    {% empty %}
                    <p>No comments here yet :(</p>

              {% endfor %}


        {% else %}
        <div class="bgi">
                {% if post.published_date %}
                    <time class="date">
                        {{ post.published_date }}
                    </time>
                {% endif %}
                <br>
                <br>
                <h2>{{ post.title }}</h2>
                <br>
                <p>{{ post.text|safe}}</p>
                <!-- <p>{{ post.text|linebreaksbr|safe}}</p> -->

                <br>
                By {{post.author.first_name}} {{post.author.last_name}}
                <!-- {{post.author.username}} -->
                <!-- here post is a context object name from PostDetailView  which can access all fields of Post model (e.g. post.text) and then we are connectig it with it's field i.e. author which is also an obj of Class User and so author can access fields of Class User i.e. username -->
                <!-- This is the way we connect different fields in different tables(Models) to get desired columns'(fields) row(data)-->
                <br><br>
                <div class="card mb-3">
                  <div class="row g-0">
                    <div class="col-md-2">
                      {% if post.author.profile.profile_pic %}
                          <img src="{{post.author.profile.profile_pic.url}}" class="img-fluid rounded-start" alt="...">
                      {% else %}
                          <img src="https://png.pngtree.com/png-vector/20190710/ourlarge/pngtree-user-vector-avatar-png-image_1541962.jpg" class="img-fluid rounded-start" alt="...">
                      {% endif %}
                    </div>
                    <div class="col-md-10">
                      <div class="card-body">
                        {% if post.author.first_name and post.author.last_name %}
                            <h5 class="card-title">{{post.author.first_name}} {{post.author.last_name}}</h5>
                        {% else %}
                            <h5 class="card-title">{{post.author.username}}</h5>
                        {% endif %}

                        <p class="small text-muted">

                              {% if post.author.profile.id %}
                                <a href="{% url 'blog:show_profile_page' post.author.profile.id %}">Profile Page</a> |
                              {% endif %}
                              {% if post.author.profile.fb_url %}
                                <a href="{{post.author.profile.fb_url}}">Facebook </a> |
                             {% endif %}
                             {% if post.author.profile.pratilipi_url%}
                                <a href="{{post.author.profile.pratilipi_url}}">Pratilipi </a> |
                             {% endif %}
                             {% if post.author.profile.linkedin_url %}
                                <a href="{{post.author.profile.linkedin_url}}">Linked In</a>
                             {% endif %}
                        </p>
                        <p class="card-text">{{post.author.profile.bio}}</p>

                      </div>
                    </div>
                  </div>
                </div>


        </div>
        <br>
        <!-- <h6>Note: Please Register and Log in to Create New Post and Comment on Posts</h6> -->
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
          <strong>Hello Writer!</strong> Please Register and Log in to Create New Post, Like and Comment on Posts.
          <!-- <button type="button" >
            <span aria-hidden="true">&times;</span></button> -->
        </div>
        <hr>
        <h4>Comments:</h4>
        <hr>
        {% for comment in post.comments.all %}

            <div class="comment">
                <div class="date">{{ comment.created_date }}</div>
                <strong>{{ comment.author }} said,</strong>
                <p>{{ comment.text|linebreaks }}</p>
            </div>
            <hr>
        {% empty %}
            <p>No comments here yet :(</p>
        {% endfor %}





      {% endif %}


    </div>




{% endblock %}
