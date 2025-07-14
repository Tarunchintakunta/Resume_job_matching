import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Button from '../common/Button';

const HeroSection = styled.section`
  height: 100vh;
  min-height: 600px;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  background: ${props => props.theme.colors.gradient};
  padding-top: 80px;
`;

const HeroContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 ${props => props.theme.spacing.lg};
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: ${props => props.theme.spacing.xl};
  align-items: center;
  position: relative;
  z-index: 1;
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: 1fr;
    text-align: center;
  }
`;

const TextContainer = styled.div`
  color: ${props => props.theme.colors.white};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    order: 2;
  }
`;

const HeroTitle = styled(motion.h1)`
  font-size: ${props => props.theme.fontSizes.xxlarge};
  font-weight: 700;
  margin-bottom: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    font-size: ${props => props.theme.fontSizes.xlarge};
  }
`;

const HeroSubtitle = styled(motion.p)`
  font-size: ${props => props.theme.fontSizes.medium};
  margin-bottom: ${props => props.theme.spacing.lg};
  opacity: 0.9;
`;

const ButtonContainer = styled(motion.div)`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    justify-content: center;
  }
`;

const ImageContainer = styled(motion.div)`
  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    order: 1;
    margin-bottom: ${props => props.theme.spacing.lg};
  }
`;

const HeroImage = styled(motion.img)`
  width: 100%;
  max-width: 600px;
`;

const BackgroundShapes = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
`;

const Shape = styled(motion.div)`
  position: absolute;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: ${props => props.theme.borderRadius.round};
`;

const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

const Hero = () => {
  return (
    <HeroSection>
      <BackgroundShapes>
        <Shape
          style={{ width: '300px', height: '300px', top: '-100px', left: '-100px' }}
          animate={{
            x: [0, 50, 0],
            y: [0, 30, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
        <Shape
          style={{ width: '200px', height: '200px', bottom: '100px', right: '100px' }}
          animate={{
            x: [0, -30, 0],
            y: [0, -50, 0],
          }}
          transition={{
            duration: 18,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
        <Shape
          style={{ width: '150px', height: '150px', bottom: '-50px', left: '30%' }}
          animate={{
            x: [0, 30, 0],
            y: [0, 30, 0],
          }}
          transition={{
            duration: 12,
            repeat: Infinity,
            repeatType: 'reverse'
          }}
        />
      </BackgroundShapes>
      
      <HeroContent>
        <TextContainer>
          <HeroTitle
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            transition={{ duration: 0.6 }}
          >
            Match the Right Talent to the Right Job
          </HeroTitle>
          <HeroSubtitle
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Streamline your hiring process with our AI-powered resume-to-job matching system.
            Find the best candidates faster and more accurately.
          </HeroSubtitle>
          <ButtonContainer
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <Button to="/dashboard" size="large">
              Get Started
            </Button>
            <Button to="#features" variant="outlined" size="large">
              Learn More
            </Button>
          </ButtonContainer>
        </TextContainer>
        
        <ImageContainer
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
        >
          <HeroImage 
            src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQkAAAC+CAMAAAARDgovAAABSlBMVEX///8iKD3/mAAiKDvm5ua+vsH/lgDQ0ND8/PwiKTkiKD75+fny8vLr6+v19fXw8PDg4ODKysra2tr2mgDV1dW5ubnCwsLMzMwAACH89Oi6u76zs7MAACKZmZmnp6cAABuNjY0AACYRGDBzc3ORkZEcITb4rkiEhIQrw31Cz5AAs18ZuXJPUFmGh40904/c19sAABNxc3uen6Xp+PEaITIAECUWHTWe2L6x4MZISUpOw44TwnE4w4ZhyJa569NXVlfS8eJmZmg72Y2J3rdryaFj1KRV1ZpwwJx1am1hY21827BI3Js1uH9omoFBQEwqvXs+OUaL0a8vMDlZWGQAAADw/via5cDG59dSTl/V9uW64M6k4saquMu9yNjN1+HesHTFonX4rT34u3bpjwucXAyUXByjYBHjlhjThhq4dhvBehQrKyv5zZn0s2Khq/PkAAASq0lEQVR4nO1d+1/ayN4eTDQJucckUAJRI6yJSCwIdFdpV9vqeWnPi7au27PtHt/3nL10z+3///XMJJFrEoK5YC3Ph1ogQzLzZOZ7m+9MAFhhhRVWWGGFFVZY4asGSRdweffZp28/HtHLrssyIaiEvqvo3x1bJ3W79/zF0bIrtBzQhPi9ouxWFP37Y9usW/aJaT0/XXatloDCtrpbEat7mqKfHb/smaZl1S1r/xWz7IplDEHZVXerqr6naaqy9/r8wjzxqLA/LbtumeLdn7+DRIgVTQQcIDkOSsvTd5Zl19HreNm1yxCv7fqf/kfXdB7grbODg36/f33dEMHRG6tuW/W3f152/TLDa7N+Uf9fTQbqQUMmvS9xfdDgTs8vzYv6xeVSq5cdXsERUH/7nJMH+uSBw+sW+IRY+kp6xTPzxLq034FGk5w5phzQH6x92Cu+BllxakKFab4D/XW/o+wBewqFRR0y9ehxbl5a9TfgQPY/TB6wH03Trl88envzRf3yon4OrgOIgFQM6BdImb7JslbLQA8SYd00tOAS7BU4RybWaWZ1Wgq+NaF78eNhP6yM3oKiwrIfudB8bkF5Ca750ELf0a/tE8t+1JLixjox7U+HjfBSYvXU7tXNR+2AfNo3bfOoic8pNgDH0El/nkmV5oARxoBPgx2B53lmCG4IegykB3Te57Zt98DBvMtXxWcmVB80IEma5jiG4Xl0MRwfVYpNnwQEleBnWzTVsFHzFsD5hW2+O2zNKyY3TuvWhTUtKNAFvVpwuCgseO37IETFxQNp1i/NF607W6Jw5nBSOStAO/s9A4S7xtHXN+bl5cmH0JMJUlrVHELm0jrzUd20e0dNLyxFPCWa1wA0+qUfJNDEG2DUVw7gODJP5ljcpdRjwIHmX2yc2vZx76bvjakGVCFPcfoHFjQboAGadGlYsA/Oj+2X34afjS6kVlEP6Q1AyIQNrQnvU6UP6LIsFEnQ6oMmU9X4yt2lm+Qb2375as7pDlOrqAenOqTAe7phAswEOM5fXcwIV+/Mp/v1E/Pm2vvIt6/6NVnYgVblNSgNmFalcOYVbIILs77/zhGSroTkkApBSsRRI65llrqgcJhg0xgjR5Z1bJ42h+FrHhQF5gcOtJrwgyqgMeKiD8xez34ReKJMmUjjMpAJ237R8E5NsqBCAXBVAgOkrRpgxMQ1MOFAesRMkPum9fLHdU9LC09rNXgVYqeNugSrAPnAC+fx/SNoWYVoUdeu+oKZAL2Tuv2Kad599IaJow3JuzcQ662fLHP/JNgF+/KZ+NE26zb4y7xiZ+wbaHlcBBf48pn4iCa6Pmi+IcwRuANwCeXE6+ASXz4TYN+66B3Pc8G2C59Q0CrE2H4ETHw6uXx78pNeCivDwy5hWyfnIUUeARNHlmleHINBmGtzwD6z7XroTPEjYAK8ti5N6xkbMj4q+g2K8vduQs7yGJi42bfrlvnT+llQAb0JjtF0Yaj7lRETTmwtLSbAj/sXsJ1ACwhvQyKeX9QvzF7oSdzwXzZM4Kld5hxS8fb4Rh34RTObFfDupXlxaYYHtjNlIjXf/AgSUbd6p+xgJoonDghwbpq2aX4MP8fjYAJ8sBAV1jPoibfGsqpI5fsKOIVDxzRP5kUmXCZSj2SmzQT4iASBaR1/AOtnZy1VEnBBbfUPdPLmlQmJsOYS8WiYAB8gFRZUlMdwEBxqLQjtkAanb6ye+Rba2c+iVfExMAGOzvehA/LWrtfPP704hfjw4jW0K83Li7pthYe0R1V8FEyg7IG39gmkwrSge9p7aaLUVGhz1XuvokyHPiYmwM1ry2m9bdn1nt2DIhR+PDk+jfTjTJmYN3cZH0ef6idQYUIfA7Fg2/vWqwgDw0GWTLDpMwFx+uJVvdfbN3twVHx7Gv13j48JBJK+oRedYM2UiYwmo++HFRN3yJSJ8ASgJSNLJvh5E+aCgDx3Jy7PF9zC2XWjLJng/GQYL+A46+pXvkALBC6K6L2G65AKHVQlgKtASm+ufQhh7G+KCNQassRAKU/zKvogqSj/w3mrqaIsCDrQSVYlFY0R067h0plQAKmqKuvGBQgRKDor4zSQ0Oc9oJISIEWVxcn0k12WzwQuyIAY1YB15AOKMdDZrnHMiAko+DjWr2UKICATupCZ0RWIjJjQGwOjaEwvQ4FQaA2XgSR+JUzgg2INy+XytTI1fSUFF3GCFJz8P1KcUC6SQLsGCI9omqJqfOGjY1e7SjdGYlsWTIjlGoZAYbnazpToU4CiiaLGoxrwGqBJXud5TRY1KDXxAgH1KwEKElAKKmzkHs8qBVgYHlRVjYSClkUTw/wt/vPtX29vf2Z/viV/vr1nLTNgorSThx3CBZZrTx6EWhTlO7EKfM8rQFRIlZClAjSxgCKxslghRUAKakEWCUkq4LIAxxEv40BlSUmiAY36BifcAsjEX2+F21uce7hMaOXcGLDilKzg3LQz7xMcD1CuMsNRQnOABCQD0OpPFmWGOIe8w8yUCKZBHG2TOhOtYn6ciVxtbob1kpA2E40tDBvvEhhmLJqYnRHSZYK5LucmmICCYueBbgqRKhPr7fYkD6hTdL++PiH0y9M8QCZq1/N/uRSkxgTd3EJWxAwTxdTWN8SEa+gkzwT/3kBDIT/NRO0q8UslhLSY6HcpiprpEbmckcWymnshJSaEYm5mZOTzudrTOWmTS0RKTLQMx9NwB0Sn5g6SbnlQCgvDIYdUCfKhcBwdUWFNaca3DD0R8qTvrFaV5aDnj0xVwIoA2um0Cr/z+X1KTBzUhj2idl267uxAYE0iYPEPKbuTQgLgVWhb85IMWFqVxhvMkqiS0D2hAS7KQCUFTS0I0I0dlhBoieZZIHEsg0tAIFnedV9FgpGBIEArhmAlgXFC7H61SImJqzEmBtDCktdFwam0PxMcainQGEDiCtDwPULWcBkf1zKwH8CG4SJQoRcvAZVWoQ/GVseYwAXovfI4LkKCcNhq3I2La5wo4CIp7kEmCFxWAKMA3c+4S4mJZnfExIS2CItHygKgIVMiCm/x0xNFd5XnnW+9oUBPRi1IJ1ThOmJ35WWcFCAvXmmcAQwBu6DP1VNiQizmqJxhGO1c3phY55x+ZPa+SEuLQkFRbEFlulOczCL++pgQyo5ZzelTExX3YCKjOUR3VWAK5o72dDZ8C+7DhJxRN0qrT0Chqd9NXoyBXrhZWUwEuhdy/qZiAqM+oU3pq4WTSZjMBEuKTCAJQU7pK+nhbkuYmpwAvvsLqDPfPPkmBP/3/3+D+Oabv6dSv0mk2CeArsz0AB8mNjcC8cuvmxtrG2vwlUr9JpEiEwILcHmy6QwxU+rJ5loQfvnNe7OxmUb9ppDi6FDH/k58NYEngURs/raZJROujkqRCX6s9X5bfgQyAYnIlIn0+oTk2YbMMDgjTGxzwQosz9DgycZE+ze8f2trv/2y9kj6xMjMLhAsTXPyVGaAp1mmmFj7/LvbI379PDrwZTNBjgtHXNQq03pEcf+bYuLzr3/8vgmb/uvntcfCxJQNNZuV6sfEBlIXf/xjbfP3PyaGzBfNxJSamM2d82FiE6mLDUjFPyaI+LKZIKeaPqs//ZhwiFhb++ckEV82E8SUFxqlT2xCdeGLACZIl17NGXgydPgUtx2u0lIcAc1sV2kg7OmA2cP9zJkR0mJial7DZ5HLLBO/BxARxAS3CxhNALqqkbDT/YsG/1KBqIDC9wKQFVJTFOgIVwW5CnaBLuqcLob6tSkxMb1Dlk+QwV93LMIEswt2uV1e14g9yERFFSsKyWoquwckHec1nYDdRK/oe3wFSBpbkXUiLPyVEhPEVGqAz92IzwS/C/aAJukseQZPJ29v4xqn6xpdgR/goBG4CkDezza9Bwh4tQqu7oVUOR0mhOkTSrN3Iy4T/O6uCrYrkIvtPRXNjmkaqwjb+h44I7jdbUnBISWgsL0rgEp1lwMyy1d8A4oekmeCl6etSQRRJWScGe8psfsEjYQyj2Y5kOninJoEnPN4ApSkRrrfOQsIvAKhYaLkmGDkUqvRH1BPg/ZxFX7otAd/6TeqOprdBN5uKjFGR7JIiIlC46q8Y3RrNYqijKDVKRhFYe2uYRiwaF8cMhEBWTDhegfxmGBaWLGNUc7UOIZRtYANMTiDQjkVlIN2p+NukPBkMwI+x6pfNMRngqx2DCyH7jdiAv3X8U8gklAeHuWWQ6/O+wc1IRabCREznOQZinLSqJy73vE9n5NTMZZoQ9V2QndeQiCzS8GJy0R1x8lOv8ugce445MIv1+MKCpHcRMZRvjhvI2A6/VVPd4jJRHPL7e8Y5Q4Np2dgVHswm3SplVGHmGACy01ncU8j/d1ch4jHxFkHw0ZpRKMWYrXBtCmFd/wS0PLl8JtOZjUXGJOJZofyZyKHtduTAX257faX3HTJdkmchDqO9ezWArn1vd/1qjsuCT4JqCgFdbSjK+AbZf+kRJSGlUg74iMGE8TTvKcwfBoIBUJtqykiycmW+lvGhNaYZGyOqMgKMZi4qmH+jfOaiOW65XKNMsrFWnApRMXDWG5+fyZaTjpyWBtz+XkFHHQD96vLFPdmgu1Qc5mIBmzrQSTu3puJfttHFdyTCso7p7en+PhO48NdyIdbk4/tWc5OwHn6xdiTMaQR5DEQ4yi4gCqroN2TCbHopxTvCWPuMycyw+JMTNnN8YAZD0NognswUekEKMX7MdFtzr9kNliUCbYIB3diREBsPZRlH4sycdZNmIl26NO8MsSCu8EQRVj5BEcH8sRaiqZppcWwDlFyXolhNv0pFIOaF6tLDg9lafFiWZJamUqYiHw+V84uEhGGheQE2U5SbyAeULx752F0ioVGR8tIlIl8h2pWWy0NJTYPDcyhVemZkuPm49BynJlpiw9pkT7BeKZEQmS0O/c3MDk16ZXZC3lA24YbnklGi9auYu1ilrDvtlD82PFBnXB+Iky046W0a0QEyCHHCiOstxYLpDfamEtEIkyUY95UbeZRjLNgNWHoqvpCVlUVOqPEYr2TLVOYN8GTgKCIvco80nJ9MZUdLxrdBL3x2O54NFGfChN8MaFh4aIYc9NHJVKpVJioGkkSEdfEjjhDlgYTpJGolb0Tc1eOiOZEGkzonUR98XLMp45GGxypMHHVTtLOjhupirqBYgpMFHZyQZN690FcYyI05XYMKTDR7CZFAkJ+7h5fT56EHY2cUZA8E3wnSSLmD45/b2z8O+Rw5AYmz4RuJMrEzrx7ura5FpZ0F3lsJc/EQehM7wzyHoKOY/Ou93lj45vgo9GfgZE4E2wxyfhMzgjKYB3iyX/+HiIoosrLFJjQFhgceSciB9Gt3bXc/TfCVswcxOhxz8SZ6C+gOfJGo4GeOlRt9rFiueszQmrv49VmgVhC0kzQncARP4utsUwxTmyi3NX8pKFuVOJVp6Lr2h0UpQRfkzMh3hv0taaKYkxrdgKFcnQxUZxKOWWqnamAOFaMl0u26DOD5ATnoCtGZCbKs8KQ7Xcm+kQ7phsaXV56SDCd8boWkYm8v7Pd2hr9Pp/rxMszIxectYOdKDlhEb1LBHR8bWu0SWQ+ZpqZvHC78MR2Q2GLUR3ywJCcPpI03Zhz44tPHRKJ9YlCMaITGqIem4bbKfJYeW4WfyjYxWe/FhYsgSiVIzIR0kjS61Z5rBPvDi3cLDbBPWtbRjQmalTACZALXnK92XwtZoymqjhYX1edqQpRLBScKR55NGXqwJnuYHku0ccFNSIyEdglODS2B47xPS+Dfx6Wu1ao2Y3EBOXXJXAnJIOMIc+xN+LVZbmpFtH6BNbxNaLd0KuKVsWhUt25bmgosnvqni8iMjFlS3hBV9K5iyjc1kfDoxjP4MtuRZQv9ChMUGir2Al4VAiOISV6wyNIqEYDueQ8pCj2RJ6atao8Khy9JzBAKsZ2Qxe3L5MF3ZnfJaDFNOsPFBxx6VoAMhQU+Xw53jhfempac34Uk6K6PvfLIYeRvbdUgIMWGUuWlxDS1lwm/B/EII7+EigsbMRzQ5csLxGa8+OYRtXnd7LjBd71iX4tXqrA9FZAywB51Z0jKvLD5dGkk0ToLEdhiALDs2wJJRMqHN18Gm8xYHI+ZQyw+TYVOi+ad9MABEmWDw+hE3A4dAM8TwC5AW5ggsZhKYIojC8RdRKnJ96MeRWyJDim6gPoEhDMYMdd7Og7nYOexYBWUYtp7hCbwZO+o6FlhOWSYFjnvaqn+hyfh9ElEJhqrdytOWmp3g4DTlIi7A7dnZ0idd0I3RUnNrgHtWWF2BhsFcuG0XZQ6xqdYrEMOdDdhMZUDZ+H0yU80NJ6q9po9vvNZqPaKhHCmEDH09segA98zsnDBJeannso0nKFFVZYYYUVVlhhhRVWSAz/BUya44v5QKzmAAAAAElFTkSuQmCC" 
            alt="Resume matching illustration"
            initial={{ y: 20 }}
            animate={{ y: [20, -20, 20] }}
            transition={{
              duration: 6,
              repeat: Infinity,
              repeatType: 'reverse',
              ease: 'easeInOut'
            }}
          />
        </ImageContainer>
      </HeroContent>
    </HeroSection>
  );
};

export default Hero;