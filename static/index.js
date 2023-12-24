let storytext = ""; 
// 绑定按钮点击事件


// 生成故事
async function generateStory() {
    const prompt = document.getElementById('storyPrompt').value;
    if (!prompt) {
        alert('请输入故事主题');
        return;
    }

    const response = await fetch('/generate_story', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ theme: prompt })
    });

    const data = await response.json();

    if (data.choices && data.choices.length > 0 && data.choices[0].message) {
        storytext = data.choices[0].message.content;
        document.getElementById('storyResult').textContent = storytext;
    } else {
        document.getElementById('storyResult').textContent = "未能生成故事";
    }
}
// 
async function fetchData(url, payload, onDataReceived) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    const reader = response.body.getReader();

    while (true) {
        const { done, value } = await reader.read();
        if (done) {
            break;
        }

        const data = new TextDecoder().decode(value);
        onDataReceived(data);
    }
}

// 生成音频

async function generateAudio() {
    if (!storytext) {
        alert('请先生成故事');
        return;
    }
    
    const response = await fetch('/generate_audio', {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain'
        },
        body: storytext
    });

    const audioUrl = await response.text();

    if (audioUrl) {
        document.getElementById('audioResult').src = '/static/output.mp3';
    } else {
        console.error('音频生成失败');
    }
}


// 生成图片
async function generateImage() {
    if (!storytext) {
        alert('请先生成故事');
        return;
    }
    
    const response = await fetch('/generate_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain'
        },
        body: storytext
    });

    const data = await response.text();

    if (response.ok) {
        const imageUrl = await response.text(); // 假设后端返回的是图片URL的纯文本
        document.getElementById('imageResult').src = imageUrl;
    } else {
        console.error('图片生成失败', await response.text());
    }
}


// 绑定事件
document.getElementById('generateStoryButton').onclick = generateStory;
document.getElementById('generateAudioButton').onclick = generateAudio;
document.getElementById('generateImageButton').onclick = generateImage;


