import { Person } from '../Types/base'

export const apiRegisterUser = async (data: any) => {
    try {
        const response = await fetch('/api/v1/user/registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.is_success) {
            alert('註冊成功!');
        } else {
            alert(`註冊失敗: ${result.msg}`);
        }
    } catch (error) {
        alert('註冊過程中出現錯誤，請稍後再試。');
    }
}


export const apiLogin = async (username: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    const response = await fetch('/api/v1/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        },
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem('user', JSON.stringify(data));
        sessionStorage.setItem('token', data.access_token);
        return true;
    } else {
        return false;
    }
}

export const fetchProfileData = async (userId: string) => {
    const token = sessionStorage.getItem('token');

    const headers = {
        'Authorization': `Bearer ${token}`,
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
    };
    const response = await fetch(`/api/v1/user/profile/${userId}`, {
        method: 'GET',
        headers: headers
    });
    if (response.ok) {
        return await response.json();
    } else {
        throw new Error('Failed to fetch user data');
    }
};


export const fetchUsersList = async () => {
    const token = sessionStorage.getItem('token');

    const headers = {
        'Authorization': `Bearer ${token}`,
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
    };
    const response = await fetch(`/api/v1/user/list`, {
        method: 'GET',
        headers: headers
    });
    if (response.ok) {
      return await response.json();
    } else {
      throw new Error('Failed to fetch users list');
    }
  };


  export const trackUser = async (trackUserId: number) => {
    const token = sessionStorage.getItem('token');

    const headers = {
        'Authorization': `Bearer ${token}`,
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json'
    };
    const response = await fetch(`/api/v1/user/track`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ track_user_id: trackUserId })
    });
    if (response.ok) {
      return await response.json();
    } else {
      throw new Error('Failed to track user');
    }
};


// Api/User.ts
export const fetchWhoCheckedMe = async () => {
    const token = sessionStorage.getItem('token');

    const headers = {
        'Authorization': `Bearer ${token}`,
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
    };

    const response = await fetch(`/api/v1/user/track`, {
        method: 'GET',
        headers: headers
    });

    if (response.ok) {
      return await response.json();
    } else {
      throw new Error('Failed to fetch who checked me list');
    }
};


// Api/User.ts

export const updateProfileData = async (data: Omit<Person, 'user_id'>) => {
    const token = sessionStorage.getItem('token');
  
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json',
    };
  
    // 根據您之前的描述，對於圖片，我們需要進行base64轉換。
    // 但在給定的敘述中，已經說明img字段是base64編碼的，所以這裡沒有再進行額外的轉換。
  
    const response = await fetch(`/api/v1/user/profile`, {
      method: 'PUT',
      headers: headers,
      body: JSON.stringify(data),
    });
  
    if (response.ok) {
      return await response.json();
    } else {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to update profile');
    }
  };
  