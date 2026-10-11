import os
import requests  # <-- Add this to your imports at the top
from flask import Flask, render_template, request, redirect, url_for, Response
from pymongo import MongoClient
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader

# ... Keep your existing setup and routes here ...

@app.route('/download/<sprite_id>')
def download_sprite(sprite_id):
    """Fetches the image from Cloudinary and forces a browser download attachment."""
    try:
        # Find the sprite in MongoDB
        sprite = sprites_collection.find_one({"_id": ObjectId(sprite_id)})
        if not sprite:
            return "Sprite not found", 404
            
        image_url = sprite.get('image_url')
        sprite_name = sprite.get('name', 'sprite')
        
        # Determine file extension from the URL (default to png if not found)
        ext = image_url.split('.')[-1] if '.' in image_url else 'png'
        filename = f"{sprite_name.replace(' ', '_')}.{ext}"

        # Stream the image file from Cloudinary
        req = requests.get(image_url, stream=True)
        
        # Return the file stream with attachment headers
        return Response(
            req.iter_content(chunk_size=1024),
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": req.headers.get("Content-Type")
            }
        )
    except Exception as e:
        return f"Download Failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
