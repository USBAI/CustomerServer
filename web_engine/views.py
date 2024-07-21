# products/views.py

from django.http import JsonResponse

def get_product(request):
    json_product = {
        
        "GetData":{
            "1":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "2":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "3":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "4":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "5":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "6":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "7":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "8":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "9":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "10":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "11":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "12":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "13":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "14":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "15":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "16":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "17":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "18":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "19":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "20":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "21":{
                "product": {
                    "name": "Sneakers",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            },
            "22":{
                "product": {
                    "name": "White Shoes",
                    "saved_in_favorites": False,
                    "price": "399,00 kr.",
                    "color": "Vit/Ljusbeige",
                    "available_colors": ["Vit/Ljusbeige", "Vit"],
                    "sizes": ["35", "36", "37", "38", "39", "40", "41", "42"]
                },
                "images": [
                    {
                        "url": "https://image.hm.com/assets/hm/a0/8c/a08c1dd2a196e373353fa523a700fbd5d846abf5.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/24/9a/249a7e35b42276584291552c6773f7886474b2c9.jpg?imwidth=2160"
                    },
                    {
                        "url": "https://image.hm.com/assets/hm/6c/2f/6c2f864a5321314551cd77a377c467fdb60fd7e3.jpg?imwidth=2160"
                    }
                ]
            }
        }
    }
    
    return JsonResponse(json_product)
