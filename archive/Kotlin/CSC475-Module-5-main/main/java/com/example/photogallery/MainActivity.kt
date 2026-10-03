package com.example.photogallery

import ImageAdapter
import android.app.Activity
import android.content.Intent
import android.database.Cursor
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.widget.Button
import android.widget.GridView

class MainActivity : Activity() {

    private lateinit var loadDeviceImagesButton: Button
    private lateinit var loadOnlineImagesButton: Button
    private lateinit var gridView: GridView
    private val imageUrls = mutableListOf<String>()
    private lateinit var imageAdapter: ImageAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        loadDeviceImagesButton = findViewById(R.id.loadDeviceImagesButton)
        loadOnlineImagesButton = findViewById(R.id.loadOnlineImagesButton)
        gridView = findViewById(R.id.imageGridView)

        imageAdapter = ImageAdapter(this, imageUrls)
        gridView.adapter = imageAdapter

        loadDeviceImagesButton.setOnClickListener { loadImagesFromDevice() }
        loadOnlineImagesButton.setOnClickListener { loadImagesFromOnline() }
    }

    private fun loadImagesFromDevice() {
        val intent = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
        startActivityForResult(intent, 1)
    }

    private fun loadImagesFromOnline() {
        val onlineImageUrls = listOf(
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg",
            "https://example.com/image3.jpg"
        )

        imageUrls.addAll(onlineImageUrls)
        imageAdapter.notifyDataSetChanged()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == 1 && resultCode == RESULT_OK && data != null) {
            val selectedImageUri: Uri? = data.data
            selectedImageUri?.let {
                val imagePath = getPathFromUri(it)
                imageUrls.add(imagePath)
                imageAdapter.notifyDataSetChanged()
            }
        }
    }

    private fun getPathFromUri(uri: Uri): String {
        val projection = arrayOf(MediaStore.Images.Media.DATA)
        val cursor: Cursor? = contentResolver.query(uri, projection, null, null, null)
        cursor?.moveToFirst()
        val columnIndex = cursor?.getColumnIndexOrThrow(MediaStore.Images.Media.DATA) ?: 0
        val filePath = cursor?.getString(columnIndex) ?: ""
        cursor?.close()
        return filePath
    }
}
