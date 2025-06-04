const modelViewerGallary = document.querySelector('#modelViewerGallary');
modelViewerGallary.isTextured = false;
// Hide the texture toggle since we only show geometry
document.querySelector('#toggleTexturedGallery').style.display = 'none';

// Set initial viewer settings for geometry-only view
modelViewerGallary.setAttribute('exposure', '0.5');
modelViewerGallary.setAttribute('shadow-intensity', '0');

// Initialize the selection panel images
$('#gallerySelectionPanel .selectable-image').each((i, img) => {
    img.src = `static/gallery/${img.getAttribute('name')}/image.jpg`;
})

// Add event listener to the selection panel
const gallerySelectionPanel = document.getElementById('gallerySelectionPanel');
gallerySelectionPanel.addEventListener('click', async function(event) {
    const img = event.target.closest('.selectable-image'); 
    
    if (!img || img.classList.contains('selected')) 
        return;
   
    gallerySelectionPanel.querySelectorAll('.selectable-image').forEach(function(image) {
        image.classList.remove('selected');
    });
    img.classList.add('selected');

    const name = img.getAttribute('name');

    // Load the model with its embedded textures
    modelViewerGallary.src = `static/gallery/${name}/mesh.glb`;
    modelViewerGallary.resetView();
    modelViewerGallary.showPoster();
});

// Set the toggle buttons
toggleGalleryLeftButton = document.querySelector('#toggleTexturedGallery .toggle-left');
toggleGalleryRightButton = document.querySelector('#toggleTexturedGallery .toggle-right');

toggleGalleryLeftButton.addEventListener('click', function() {
    toggleGalleryLeftButton.classList.add('active');
    toggleGalleryRightButton.classList.remove('active');
    modelViewerGallary.setAttribute('exposure', '0.5'); // Adjust exposure for better visibility
    modelViewerGallary.setAttribute('shadow-intensity', '0'); // Disable shadows for untextured view
});

toggleGalleryRightButton.addEventListener('click', function() {
    toggleGalleryRightButton.classList.add('active');
    toggleGalleryRightButton.classList.remove('active');
    modelViewerGallary.setAttribute('exposure', '1'); // Normal exposure for textured view
    modelViewerGallary.setAttribute('shadow-intensity', '1'); // Enable shadows for textured view
});

// Initialize the model viewer with selected model
$(document).ready(() => {
    const name = document.querySelector('#gallerySelectionPanel .selectable-image.selected').getAttribute('name');

    // Load the model with its embedded textures
    modelViewerGallary.src = `static/gallery/${name}/mesh.glb`;
    modelViewerGallary.resetView();
    modelViewerGallary.showPoster();
});