from django.db import models

# Create your models here.
class PromptHistory(models.Model):
    original_prompt = models.TextField()
    optimized_prompt = models.TextField()
    quality_score = models.IntegerField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_prompt[:40]