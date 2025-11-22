from django import forms
from django.forms.widgets import Widget


class StyledTextInput(forms.TextInput):
    """Custom styled text input widget"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control styled-input',
            'style': 'width: 100%; max-width: 500px; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class StyledTextarea(forms.Textarea):
    """Custom styled textarea widget"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control styled-textarea',
            'style': 'width: 100%; max-width: 500px; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; min-height: 120px;',
            'rows': 5
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class StyledSelect(forms.Select):
    """Custom styled select widget"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control styled-select',
            'style': 'width: 100%; max-width: 500px; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class StyledNumberInput(forms.NumberInput):
    """Custom styled number input widget"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control styled-number',
            'style': 'width: 100%; max-width: 200px; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class StyledFileInput(forms.ClearableFileInput):
    """Custom styled file input widget"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control styled-file',
            'style': 'padding: 12px; border: 2px dashed #d1d5db; border-radius: 8px; background-color: #f9fafb;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
