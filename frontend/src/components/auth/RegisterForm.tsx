import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';

export const RegisterForm = ({ onRegister }: { onRegister: (values: { username: string; email: string; password: string }) => Promise<void> }) => {
  const [form] = Form.useForm();

  const handleSubmit = async (values: { username: string; email: string; password: string }) => {
    try {
      await onRegister(values);
    } catch (error) {
      message.error('注册失败，请重试');
    }
  };

  return (
    <Form form={form} onFinish={handleSubmit}>
      <Form.Item name="username" rules={[{ required: true, message: '请输入用户名' }]}>
        <Input prefix={<UserOutlined />} placeholder="用户名" />
      </Form.Item>
      <Form.Item name="email" rules={[
        { required: true, message: '请输入邮箱' },
        { type: 'email', message: '请输入有效的邮箱地址' }
      ]}>
        <Input prefix={<MailOutlined />} placeholder="邮箱" />
      </Form.Item>
      <Form.Item name="password" rules={[{ required: true, message: '请输入密码' }]}>
        <Input.Password prefix={<LockOutlined />} placeholder="密码" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" block>注册</Button>
      </Form.Item>
    </Form>
  );
};
