// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State
let currentAudio = null;
let currentStoryData = null;
let storyHistory = []; // Track story progression

// Set theme from quick action button
function setTheme(theme) {
    document.getElementById('themeInput').value = theme;
    generateStory();
}

// Handle Enter key press in input
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        generateStory();
    }
}

// Generate story
async function generateStory() {
    const themeInput = document.getElementById('themeInput');
    const theme = themeInput.value.trim();

    if (!theme) {
        showError('Please enter a theme for your story');
        return;
    }

    // Reset story history for new story
    storyHistory = [];

    // Hide previous content
    hideError();
    hideStory();
    
    // Show loading state
    showLoading();

    try {
        // Call the API
        const response = await fetch(`${API_BASE_URL}/story/generate?theme=${encodeURIComponent(theme)}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate story');
        }

        const data = await response.json();
        currentStoryData = data;
        
        // Add to history
        storyHistory.push({
            story: data.story,
            choices: data.choices
        });

        // Hide loading and show story
        hideLoading();
        displayStory(data);

    } catch (error) {
        hideLoading();
        showError(`Error: ${error.message}. Please try again.`);
        console.error('Error generating story:', error);
    }
}

// Continue story with chosen option
async function continueStory(choiceText) {
    // Show loading state
    showLoading();
    hideStory();

    try {
        // Build story context from history
        const storyContext = storyHistory.map(h => h.story).join('\n\n');
        
        // Call the continue API
        const response = await fetch(`${API_BASE_URL}/story/continue`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                theme: currentStoryData.theme,
                choice: choiceText,
                story_context: storyContext
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to continue story');
        }

        const data = await response.json();
        currentStoryData = data;
        
        // Add to history
        storyHistory.push({
            story: data.story,
            choices: data.choices
        });

        // Hide loading and show story
        hideLoading();
        displayStory(data, true); // true = append mode

    } catch (error) {
        hideLoading();
        showError(`Error: ${error.message}. Please try again.`);
        console.error('Error continuing story:', error);
    }
}

// Display the generated story
function displayStory(data, append = false) {
    const storyContainer = document.getElementById('storyContainer');
    const storyTheme = document.getElementById('storyTheme');
    const storyText = document.getElementById('storyText');
    const audioPlayer = document.getElementById('audioPlayer');
    const audioElement = document.getElementById('audioElement');

    // Debug logging
    console.log('Displaying story:', data);
    console.log('Story text length:', data.story ? data.story.length : 0);

    // Set content
    storyTheme.textContent = data.theme || 'Your Story';
    
    if (append) {
        // Append new segment to existing story
        storyText.textContent += '\n\n' + (data.story || '');
    } else {
        // New story
        storyText.textContent = data.story || 'Story loading...';
    }
    
    console.log('Story element updated with', storyText.textContent.length, 'characters');

    // Display illustration in left page
    displayIllustration(data.image_description);

    // Set up audio if available
    if (data.voice_file) {
        audioElement.src = `${API_BASE_URL}/${data.voice_file}`;
        audioPlayer.style.display = 'block';
        
        // Setup audio listeners
        audioElement.addEventListener('loadedmetadata', updateDuration);
    } else {
        audioPlayer.style.display = 'none';
    }

    // Display choices if available
    displayChoices(data.choices);

    // Show story container
    storyContainer.style.display = 'block';
    
    // Scroll to story
    setTimeout(() => {
        storyContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Display illustration in right page
function displayIllustration(imageDescription) {
    const illustrationContainer = document.getElementById('illustrationContainer');
    
    console.log('Image description:', imageDescription);
    
    if (imageDescription && imageDescription.trim() && imageDescription !== "Image generation unavailable") {
        illustrationContainer.innerHTML = `
            <div class="illustration-description">
                <p>${imageDescription}</p>
            </div>
        `;
    } else {
        illustrationContainer.innerHTML = `
            <div class="illustration-placeholder">
                <span class="placeholder-icon">🎨</span>
                <p class="placeholder-text">Generating illustration...</p>
            </div>
        `;
    }
}

// Display choice buttons
function displayChoices(choices) {
    const storyActions = document.querySelector('.story-actions');
    
    // Clear existing choice buttons (keep share and new story buttons)
    const choiceButtons = storyActions.querySelectorAll('.choice-button');
    choiceButtons.forEach(btn => btn.remove());
    
    if (choices && choices.length > 0) {
        // Create a choices container
        let choicesContainer = document.getElementById('choicesContainer');
        if (!choicesContainer) {
            choicesContainer = document.createElement('div');
            choicesContainer.id = 'choicesContainer';
            choicesContainer.className = 'choices-container';
            // Insert before story actions
            storyActions.parentNode.insertBefore(choicesContainer, storyActions);
        }
        
        choicesContainer.innerHTML = '<h3 class="choices-title">What happens next?</h3>';
        
        choices.forEach((choice, index) => {
            const button = document.createElement('button');
            button.className = 'choice-button';
            button.textContent = choice;
            button.onclick = () => continueStory(choice);
            choicesContainer.appendChild(button);
        });
    } else {
        // Remove choices container if no choices
        const choicesContainer = document.getElementById('choicesContainer');
        if (choicesContainer) {
            choicesContainer.remove();
        }
    }
}

// Toggle audio playback
function toggleAudio() {
    const audioElement = document.getElementById('audioElement');
    const playIcon = document.getElementById('playIcon');

    if (audioElement.paused) {
        audioElement.play();
        playIcon.textContent = '⏸';
    } else {
        audioElement.pause();
        playIcon.textContent = '▶';
    }
}

// Rewind audio by 10 seconds
function rewindAudio() {
    const audioElement = document.getElementById('audioElement');
    audioElement.currentTime = Math.max(0, audioElement.currentTime - 10);
}

// Forward audio by 10 seconds
function forwardAudio() {
    const audioElement = document.getElementById('audioElement');
    audioElement.currentTime = Math.min(audioElement.duration, audioElement.currentTime + 10);
}

// Seek to specific position in audio
function seekAudio(event) {
    const audioElement = document.getElementById('audioElement');
    const progressBar = event.currentTarget;
    const clickX = event.offsetX;
    const width = progressBar.offsetWidth;
    const seekTime = (clickX / width) * audioElement.duration;
    
    audioElement.currentTime = seekTime;
}

// Update audio progress bar and time display
function updateAudioProgress() {
    const audioElement = document.getElementById('audioElement');
    const progressBar = document.getElementById('progressBar');
    const currentTimeEl = document.getElementById('currentTime');
    
    if (audioElement.duration) {
        const progress = (audioElement.currentTime / audioElement.duration) * 100;
        progressBar.style.width = `${progress}%`;
        currentTimeEl.textContent = formatTime(audioElement.currentTime);
    }
}

// Update duration display
function updateDuration() {
    const audioElement = document.getElementById('audioElement');
    const durationEl = document.getElementById('duration');
    
    if (audioElement.duration) {
        durationEl.textContent = formatTime(audioElement.duration);
    }
}

// Format time in MM:SS
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Reset audio button when audio ends
function resetAudioButton() {
    const playIcon = document.getElementById('playIcon');
    const progressBar = document.getElementById('progressBar');
    
    playIcon.textContent = '▶';
    progressBar.style.width = '0%';
}

// Share story
function shareStory() {
    if (!currentStoryData) return;

    const shareText = `Check out this AI-generated story about "${currentStoryData.theme}":\n\n${currentStoryData.story}`;
    
    if (navigator.share) {
        navigator.share({
            title: `A Story About ${currentStoryData.theme}`,
            text: shareText,
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(shareText).then(() => {
            alert('Story copied to clipboard!');
        }).catch(err => {
            console.error('Could not copy text:', err);
        });
    }
}

// Create new story
function newStory() {
    const themeInput = document.getElementById('themeInput');
    const audioElement = document.getElementById('audioElement');
    
    // Reset form
    themeInput.value = '';
    themeInput.focus();
    
    // Stop audio if playing
    if (audioElement) {
        audioElement.pause();
        audioElement.currentTime = 0;
        resetAudioButton();
    }
    
    // Hide story
    hideStory();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show/Hide functions
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

function showStory() {
    document.getElementById('storyContainer').style.display = 'block';
}

function hideStory() {
    document.getElementById('storyContainer').style.display = 'none';
}

function showError(message) {
    const errorElement = document.getElementById('errorMessage');
    errorElement.textContent = message;
    errorElement.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Focus on input
    document.getElementById('themeInput').focus();
    
    // Add some example themes on page load
    console.log('BridgeTales AI Storyteller loaded successfully!');
});
