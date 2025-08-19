const About = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-center text-gray-900 mb-12">
        About MediCheck
      </h1>
      
      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">How Our AI Works</h2>
        <p className="text-gray-600 mb-6">
          MediCheck uses advanced AI technology powered by medical language models to analyze your symptoms 
          and provide preliminary health insights. Our system processes your input along with demographic 
          information to generate relevant possible diagnoses and recommendations.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="text-center p-6 bg-blue-50 rounded-lg">
            <div className="text-4xl mb-3">🤖</div>
            <h3 className="font-semibold mb-2">AI-Powered</h3>
            <p className="text-sm text-gray-600">Advanced medical AI models</p>
          </div>
          <div className="text-center p-6 bg-green-50 rounded-lg">
            <div className="text-4xl mb-3">⚡</div>
            <h3 className="font-semibold mb-2">Instant Results</h3>
            <p className="text-sm text-gray-600">Get insights in seconds</p>
          </div>
          <div className="text-center p-6 bg-purple-50 rounded-lg">
            <div className="text-4xl mb-3">🔒</div>
            <h3 className="font-semibold mb-2">Privacy First</h3>
            <p className="text-sm text-gray-600">Your data stays secure</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Privacy Policy</h2>
        <div className="space-y-4 text-gray-600">
          <p>
            We take your privacy seriously. Your symptom data is processed securely and is not stored 
            permanently on our servers.
          </p>
          <ul className="list-disc list-inside space-y-2">
            <li>No personal health information is permanently stored</li>
            <li>All communications are encrypted</li>
            <li>We do not share your data with third parties</li>
            <li>Session data is automatically cleared after use</li>
          </ul>
          <p className="text-sm text-yellow-700 bg-yellow-50 p-3 rounded-lg">
            <strong>Important:</strong> This tool is for informational purposes only and should not replace 
            professional medical advice, diagnosis, or treatment.
          </p>
        </div>
      </div>
    </div>
  )
}

export default About