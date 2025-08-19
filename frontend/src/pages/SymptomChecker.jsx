import { useState } from 'react'
import axios from 'axios'

const SymptomChecker = () => {
  const [formData, setFormData] = useState({
    symptoms: '',
    age_group: '',
    gender: ''
  })
  const [githubUsername, setGithubUsername] = useState('')
  const [isVerified, setIsVerified] = useState(false)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [verifyLoading, setVerifyLoading] = useState(false)

  const verifyGitHubStar = async () => {
    if (!githubUsername.trim()) {
      alert('Please enter your GitHub username')
      return
    }
    setVerifyLoading(true)
    
    try {
      const response = await axios.post('/verify-star', { github_username: githubUsername.trim() })
      console.log('Verification response:', response.data)
      
      if (response.data.starred) {
        setIsVerified(true)
        alert('✅ Verification successful! You can now use the symptom checker.')
      } else {
        alert(`❌ ${response.data.message}\n\nPlease star the repository: https://github.com/sanatanisher01/Healthcare-symptoms`)
      }
    } catch (error) {
      console.error('Verification error:', error)
      alert('❌ Unable to verify. Please check your username and try again.')
    } finally {
      setVerifyLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!isVerified) {
      alert('Please verify your GitHub star first!')
      return
    }
    
    setLoading(true)
    
    try {
      const response = await axios.post(`/check-symptoms?github_username=${encodeURIComponent(githubUsername.trim())}`, formData)
      setResults(response.data)
    } catch (error) {
      console.error('Error:', error)
      if (error.response?.status === 403) {
        alert('❌ Star verification failed. Please star the repository: https://github.com/sanatanisher01/Healthcare-symptoms')
        setIsVerified(false)
      } else {
        setResults({
          diagnoses: ['Unable to process request'],
          recommendations: ['Please try again later or consult a healthcare professional']
        })
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-center text-gray-900 mb-12">
        AI Symptom Checker
      </h1>
      
      {!isVerified && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 mb-8 rounded-lg">
          <h2 className="text-xl font-semibold text-yellow-800 mb-4">⭐ Star Required</h2>
          <p className="text-yellow-700 mb-4">
            Please star our repository to access the AI symptom checker:
          </p>
          <a 
            href="https://github.com/sanatanisher01/Healthcare-symptoms" 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-block bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 mb-4"
          >
            ⭐ Star Repository
          </a>
          
          <div className="mb-3">
            <p className="text-sm text-yellow-700 mb-2">
              <strong>Username Format:</strong> Enter only your GitHub username (not full URL)
            </p>
            <p className="text-xs text-yellow-600">
              ✅ Correct: <code className="bg-yellow-100 px-1 rounded">sanatanisher01</code><br/>
              ❌ Wrong: <code className="bg-red-100 px-1 rounded">https://github.com/sanatanisher01</code>
            </p>
          </div>
          
          <div className="flex gap-2">
            <input
              type="text"
              value={githubUsername}
              onChange={(e) => setGithubUsername(e.target.value)}
              placeholder="username (e.g., sanatanisher01)"
              className="flex-1 p-3 border border-gray-300 rounded-lg"
            />
            <button
              type="button"
              onClick={verifyGitHubStar}
              disabled={verifyLoading || !githubUsername}
              className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              {verifyLoading ? 'Verifying...' : 'Verify'}
            </button>
          </div>
        </div>
      )}

      <div className={`bg-white rounded-2xl shadow-xl p-8 mb-8 ${!isVerified ? 'opacity-50 pointer-events-none' : ''}`}>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe your symptoms
            </label>
            <textarea
              value={formData.symptoms}
              onChange={(e) => setFormData({...formData, symptoms: e.target.value})}
              className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              rows="4"
              placeholder="e.g., fever, cough, sore throat, headache..."
              required
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Age Group
              </label>
              <select
                value={formData.age_group}
                onChange={(e) => setFormData({...formData, age_group: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                required
              >
                <option value="">Select age group</option>
                <option value="Child">Child (0-12)</option>
                <option value="Teen">Teen (13-19)</option>
                <option value="Adult">Adult (20-64)</option>
                <option value="Senior">Senior (65+)</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gender
              </label>
              <select
                value={formData.gender}
                onChange={(e) => setFormData({...formData, gender: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                required
              >
                <option value="">Select gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
          
          <button
            type="submit"
            disabled={loading || !isVerified}
            className="w-full bg-primary text-white py-4 px-6 rounded-lg font-semibold hover:bg-blue-700 transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-2"></div>
                Analyzing...
              </div>
            ) : isVerified ? (
              'Check Symptoms'
            ) : (
              '⭐ Star Repository First'
            )}
          </button>
        </form>
      </div>

      {results && (
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Results</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                <span className="text-2xl mr-2">🔍</span>
                Possible Diagnoses
              </h3>
              <div className="space-y-2">
                {results.diagnoses.map((diagnosis, index) => (
                  <div key={index} className="bg-blue-50 p-3 rounded-lg border-l-4 border-primary">
                    {diagnosis}
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                <span className="text-2xl mr-2">💡</span>
                Recommended Next Steps
              </h3>
              <div className="space-y-2">
                {results.recommendations.map((recommendation, index) => (
                  <div key={index} className="bg-green-50 p-3 rounded-lg border-l-4 border-green-500">
                    {recommendation}
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="mt-8 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg">
            <p className="text-sm text-yellow-800">
              <strong>Disclaimer:</strong> This is not a medical diagnosis. Please consult a doctor for proper medical advice.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default SymptomChecker