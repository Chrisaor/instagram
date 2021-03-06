from django.contrib.auth.models import AbstractUser
from django.db import models

from members.exception import RelationNotExist, DuplicateRelationException


class User(AbstractUser):
    CHOICE_GENDER = (
        ('m', '남성'),
        ('f', '여성'),
        ('x', '선택안함')
    )
    img_profile = models.ImageField(upload_to='user', blank=True)
    site = models.URLField(blank=True)
    introduce = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICE_GENDER)
    to_relation_users = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        blank=True,
        related_name='from_relation_users',
        related_query_name='from_relation_user',
    )

    def __str__(self):
        return self.username


    @property
    def following(self):
        return User.objects.filter(
            relation_by_to_user__from_user=self,
            relation_by_to_user__relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def followers(self):
        return User.objects.filter(
            relation_by_from_user__to_user=self,
            relation_by_from_user__relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    # @property
    # def block_user(self):
    #     return User.objects.filter(
    #         relation_by_from_user__to_user=self,
    #         relation_by_from_user__relation_type=Relation.RELATION_TYPE_BLOCK,
    #     )

    @property
    def following_relations(self):
        return self.relation_by_from_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def follower_relations(self):
        return self.relation_by_to_user.filter(
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    @property
    def block_relations(self):
        return self.relation_by_to_user.filter(
            relation_type=Relation.RELATION_TYPE_BLOCK,
        )

    def follow(self, to_user):


        if self.relation_by_from_user.filter(
            to_user__in=to_user).exists():
            raise DuplicateRelationException(from_user=self,to_user=to_user,relation_type='follow')

        return self.relation_by_from_user.create(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW,
        )

    def unfollow(self, to_user):
        q = self.relation_by_from_user.filter(
            to_user=to_user,
            relation_type=Relation.RELATION_TYPE_FOLLOW
        )

        if q:
            q.delete()
        else:
            raise RelationNotExist(
                from_user=self,
                to_user=to_user,
                relation_type='Follow',
            )

class Relation(models.Model):
    RELATION_TYPE_BLOCK = 'b'
    RELATION_TYPE_FOLLOW = 'f'
    CHOICES_RELATION_TYPE = (
        (RELATION_TYPE_FOLLOW, 'Follow'),
        (RELATION_TYPE_BLOCK, 'Block',),
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relation_by_from_user'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='relation_by_to_user'
    )
    relation_type = models.CharField(max_length=1, choices=CHOICES_RELATION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )

    def __str__(self):
        return 'From {from_user} to {to_user} ({type})'.format(
            from_user=self.from_user.username,
            to_user=self.to_user.username,
            type=self.get_relation_type_display()
        )
