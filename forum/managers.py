from django.db import connection, models, transaction

class TagManager(models.Manager):
    UPDATE_USED_COUNTS_QUERY = (
        'UPDATE tag '
        'SET used_count = ('
            'SELECT COUNT(*) FROM post_tags '  # noqa
            'WHERE tag_id = tag.id'  # noqa
        ') '
        'WHERE id IN (%s)')

    def get_valid_tags(self, page_size):
        import forum.models.Tag  # noqa
        tags = Tag.objects.all().filter(deleted=False).exclude(used_count=0).order_by("-id")[:page_size]  # noqa
        return tags

    def get_or_create_multiple(self, names, user):
        """
        Fetches a list of Tags with the given names, creating any Tags
        which don't exist when necesssary.
        """
        tags = list(self.filter(name__in=names))
        # Set all these tag visible
        for tag in tags:
            if tag.deleted:
                tag.deleted = False
                tag.deleted_by = None
                tag.deleted_at = None
                tag.save()
        if len(tags) < len(names):
            existing_names = set(tag.name for tag in tags)
            new_names = [name for name in names if name not in existing_names]
            tags.extend([self.create(name=name, author=user)
                         for name in new_names if self.filter(name=name).count() == 0 and len(name.strip()) > 0])
        return tags

    def update_use_counts(self, tags):
        """Updates the given Tags with their current use counts."""
        if not tags:
            return
        cursor = connection.cursor()
        query = self.UPDATE_USED_COUNTS_QUERY % ','.join(['%s'] * len(tags))
        cursor.execute(query, [tag.id for tag in tags])
        transaction.commit_unless_managed()

    def get_tags_by_posts(self, posts):
        post_ids = []
        for post in posts:
            post_ids.append(post.id)

        post_ids_str = ','.join([str(id) for id in post_ids])
        related_tags = self.extra(
            tables=['tag', 'post_tags'],
            where=["tag.id = post_tags.tag_id AND post_tags.post_id IN (" + post_ids_str + ")"]
        ).distinct()

        return related_tags
