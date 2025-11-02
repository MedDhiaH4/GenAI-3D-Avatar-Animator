// Import the libraries we defined in our importmap
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// 1. Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xdddddd);

// 2. Camera setup
// ... (all the same code)
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;
camera.position.y = 2;

// 3. Renderer setup
// ... (all the same code)
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 4. Add Lights
// ... (all the same code)
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(0, 5, 5);
scene.add(directionalLight);

// 5. Add Camera Controls
// ... (all the same code)
const controls = new OrbitControls(camera, renderer.domElement);
controls.update();

// 6. Load the Avatar!
const loader = new GLTFLoader();

// --- !!! IMPORTANT CHANGE !!! ---
// The path is now relative to the /static/ folder
// as defined in main.py
loader.load(
    '/static/avatar.glb',
    
    // --- This function runs when the model is LOADED
    function (gltf) {
        const model = gltf.scene;
        scene.add(model);
        
        console.log('Model loaded successfully!');

        // --- !!! ADD THIS NEW CODE BELOW !!! ---

        console.log("--- AVATAR SKELETON BONE LIST ---");
        
        // We'll use an array to store the names for a clean list
        const boneNames = []; 
        
        // The .traverse() method visits every object in the 3D model
        model.traverse(function(object) {
            // We check if the object is a 'Bone'
            if (object.isBone) {
                // If it is, we add its name to our list
                boneNames.push(object.name);
            }
        });
        
        // Log the complete list to the console
        console.log(boneNames);
        
        // We'll also log the full skeleton structure
        // This is very useful for seeing the parent/child hierarchy
        console.log("Full skeleton structure:", model.children);

        console.log("-----------------------------------");
        
        // --- END OF NEW CODE ---
    },
    
    // --- This function runs during loading (for progress bars)
    function (xhr) {
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    
    // --- This function runs if there is an ERROR
    function (error) {
        console.error('An error happened while loading the model:', error);
    }
);

// 7. The Animation Loop
// ... (all the same code)
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

// Handle window resizing
// ... (all the same code)
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Start the animation loop!
animate();